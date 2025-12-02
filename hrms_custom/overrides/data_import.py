"""
Custom Data Import override - Convert all warnings to row-level errors.

Goal:
- Convert ALL template warnings into row-level failures during import
- Allow import to proceed even with data issues
- Failed rows appear in Export Errored Rows instead of blocking entire import
"""

from __future__ import annotations

import json
import frappe
import timeit
from rq.timeouts import JobTimeoutException
from frappe.core.doctype.data_import.data_import import DataImport as OriginalDataImport
from frappe.core.doctype.data_import.importer import Importer
from frappe.utils.background_jobs import enqueue, is_job_enqueued


class CustomDataImport(OriginalDataImport):
	"""Override of Frappe's Data Import DocType controller.
	
	- Uses custom importer that converts warnings to row-level errors
	- Allows import to proceed and collect all errors per row
	"""

	def start_import(self):
		from frappe.utils.scheduler import is_scheduler_inactive

		run_now = frappe.in_test or frappe.conf.developer_mode
		if is_scheduler_inactive() and not run_now:
			frappe.throw(frappe._("Scheduler is inactive. Cannot import data."), title=frappe._("Scheduler Inactive"))

		job_id = f"data_import||{self.name}"

		if not is_job_enqueued(job_id):
			enqueue(
				worker_start_import,
				queue="default",
				timeout=10000,
				event="data_import",
				job_id=job_id,
				data_import=self.name,
				now=run_now,
			)
			frappe.logger().info(
				f"[hrms_custom] Enqueued Custom Data Import job (Data Import: {self.name})"
			)
			return True

		return False

	def get_importer(self):
		"""Return custom importer that handles warnings as row errors."""
		return CustomImporter(self.reference_doctype, data_import=self, use_sniffer=self.use_csv_sniffer)


def worker_start_import(data_import: str):
	"""Background job entrypoint with custom importer."""
	data_import_doc = frappe.get_doc("Data Import", data_import)
	try:
		importer = CustomImporter(data_import_doc.reference_doctype, data_import=data_import_doc)
		importer.import_data()
	except JobTimeoutException:
		frappe.db.rollback()
		data_import_doc.db_set("status", "Timed Out")
	except Exception:
		frappe.db.rollback()
		data_import_doc.db_set("status", "Error")
		data_import_doc.log_error("Data import failed")
	finally:
		frappe.flags.in_import = False

	frappe.publish_realtime("data_import_refresh", {"data_import": data_import_doc.name})


class CustomImporter(Importer):
	"""
	Custom Importer that converts ALL warnings to row-level errors.
	
	Instead of blocking entire import with template warnings:
	- Import proceeds with all rows
	- Validation happens per row during processing
	- Failed rows are logged and exported via Export Errored Rows
	"""

	def import_data(self):
		"""Modified import_data that ignores template warnings and validates per row."""
		self.before_import()

		payloads = self.import_file.get_payloads_for_import()

		# MODIFIED: Ignore ALL warnings - we'll validate per row instead
		warnings = self.import_file.get_warnings()
		warnings = [w for w in warnings if w.get("type") != "info"]
		
		# Store warnings for row-level validation but don't block import
		self.template_warnings = warnings

		# Continue with import (removed the blocking if warnings: return)

		import_log = (
			frappe.get_all(
				"Data Import Log",
				fields=["row_indexes", "success", "log_index"],
				filters={"data_import": self.data_import.name},
				order_by="log_index",
			)
			or []
		)

		log_index = 0

		if (
			self.data_import.status in ("Partial Success", "Error")
			and len(import_log) >= self.data_import.payload_count
		):
			import_log = [log for log in import_log if log.get("success")]
			frappe.db.delete("Data Import Log", {"success": 0, "data_import": self.data_import.name})

		imported_rows = []
		for log in import_log:
			log = frappe._dict(log)
			if log.success or len(import_log) < self.data_import.payload_count:
				imported_rows += json.loads(log.row_indexes)

			log_index = log.log_index

		total_payload_count = len(payloads)
		batch_size = frappe.conf.data_import_batch_size or 1000

		for batch_index, batched_payloads in enumerate(frappe.utils.create_batch(payloads, batch_size)):
			for i, payload in enumerate(batched_payloads):
				doc = payload.doc
				row_indexes = [row.row_number for row in payload.rows]
				current_index = (i + 1) + (batch_index * batch_size)

				if set(row_indexes).intersection(set(imported_rows)):
					if total_payload_count > 5:
						frappe.publish_realtime(
							"data_import_progress",
							{
								"current": current_index,
								"total": total_payload_count,
								"skipping": True,
								"data_import": self.data_import.name,
							},
							user=frappe.session.user,
						)
					continue

				try:
					# CUSTOM: Validate row against template warnings
					self._validate_row(payload)
					
					start = timeit.default_timer()
					doc = self.process_doc(doc)
					processing_time = timeit.default_timer() - start
					eta = self.get_eta(current_index, total_payload_count, processing_time)

					if self.console:
						from frappe.utils import update_progress_bar
						update_progress_bar(
							f"Importing {self.doctype}: {total_payload_count} records",
							current_index - 1,
							total_payload_count,
						)
					elif total_payload_count > 5:
						frappe.publish_realtime(
							"data_import_progress",
							{
								"current": current_index,
								"total": total_payload_count,
								"docname": doc.name,
								"data_import": self.data_import.name,
								"success": True,
								"row_indexes": row_indexes,
								"eta": eta,
							},
							user=frappe.session.user,
						)

					from frappe.core.doctype.data_import.importer import create_import_log

					create_import_log(
						self.data_import.name,
						log_index,
						{"success": True, "docname": doc.name, "row_indexes": row_indexes},
					)

					log_index += 1

					if self.data_import.status != "Partial Success":
						self.data_import.db_set("status", "Partial Success")

					frappe.db.commit()

				except Exception as e:
					messages = frappe.local.message_log
					frappe.clear_messages()

					frappe.db.rollback()

					from frappe.core.doctype.data_import.importer import create_import_log

					create_import_log(
						self.data_import.name,
						log_index,
						{
							"success": False,
							"exception": frappe.get_traceback(),
							"messages": messages,
							"row_indexes": row_indexes,
						},
					)

					log_index += 1

		import_log = (
			frappe.get_all(
				"Data Import Log",
				fields=["row_indexes", "success", "log_index"],
				filters={"data_import": self.data_import.name},
				order_by="log_index",
			)
			or []
		)

		successes = []
		failures = []
		for log in import_log:
			if log.get("success"):
				successes.append(log)
			else:
				failures.append(log)
		if len(failures) >= total_payload_count and len(successes) == 0:
			status = "Error"
		elif len(failures) > 0 and len(successes) > 0:
			status = "Partial Success"
		elif len(successes) == total_payload_count:
			status = "Success"
		else:
			status = "Pending"

		if self.console:
			self.print_import_log(import_log)
		else:
			self.data_import.db_set("status", status)

		self.after_import()

		return import_log

	def _validate_row(self, payload):
		"""
		Validate a single row against template warnings.
		Raises exceptions for validation errors, causing row to fail and be logged.
		"""
		if not hasattr(self, 'template_warnings') or not self.template_warnings:
			return
		
		# Get row data
		if not payload.rows:
			return
		
		row_data = payload.rows[0]
		row_number = row_data.row_number if hasattr(row_data, 'row_number') else 'Unknown'
		
		# Check for warnings related to this row's data
		errors = []
		
		# 1. Check template warnings (both row-level and column-level)
		for warning in self.template_warnings:
			# Skip info warnings
			if warning.get("type") == "info":
				continue
			
			warning_row = warning.get("row")
			
			# Row-specific warning - must match exactly
			if warning_row and warning_row != row_number:
				continue
			
			# Column-level warning (no row field) - check if applies to this row's data
			if not warning_row:
				# Column warnings are about invalid values in a specific field
				message = warning.get("message", "")
				
				# Parse for "do not exist" warnings - these contain the invalid values
				if "do not exist" in message and ":" in message:
					# Extract the invalid values from message
					# Format: "The following values do not exist for {doctype}: {value1}, {value2}"
					parts = message.split(":")
					if len(parts) >= 2:
						invalid_values_str = parts[-1].strip()
						# Split by comma and normalize
						invalid_values = [v.strip().lower() for v in invalid_values_str.split(",")]
						
						# Get field info from warning
						field_info = warning.get("field", {})
						if isinstance(field_info, dict):
							fieldname = field_info.get("fieldname")
							
							if fieldname:
								# Get actual row value for this field from payload.doc
								# payload.doc has the parsed document with field values
								doc = payload.doc
								row_value = doc.get(fieldname) if isinstance(doc, dict) else None
								
								# Only error if this row's value is in the invalid list
								if row_value:
									row_value_normalized = str(row_value).strip().lower()
									
									# DEBUG: Print to console for debugging
									print(f"\n[DEBUG] Row {row_number} - Field: {fieldname}")
									print(f"  Row value: '{row_value}' (normalized: '{row_value_normalized}')")
									print(f"  Invalid values: {invalid_values}")
									print(f"  Match: {row_value_normalized in invalid_values}")
									
									if row_value_normalized in invalid_values:
										# This row actually uses an invalid value
										errors.append(message)
				else:
					# Other column warnings without specific invalid values
					# Skip these - they'll be caught during actual save
					pass
				continue
			
			# Row-level warning matched
			message = warning.get("message", "")
			if message:
				errors.append(message)
		
		# 2. Check row's own warnings
		if hasattr(row_data, 'warnings') and row_data.warnings:
			for row_warning in row_data.warnings:
				if row_warning.get("type") != "info":
					msg = row_warning.get("message", "")
					if msg and msg not in errors:
						errors.append(msg)
		
		# Raise validation error if any issues found
		if errors:
			error_msg = f"Row {row_number} validation failed:\n" + "\n".join(f"  • {e}" for e in errors)
			frappe.throw(error_msg, exc=frappe.ValidationError)
