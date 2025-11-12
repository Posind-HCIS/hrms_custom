# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


def get_permission_query_conditions(user=None):
	"""Contoh logika yang lebih kompleks (server-side list restriction).

	- Administrator/System Manager: tidak dibatasi.
	- User lain: hanya record dengan
	  (alamat = 'Tidak Tersedia') ATAU (owner = user saat ini).

	Tambahkan kondisi lain sesuai kebutuhan (mis. tanggal, status) ke dalam OR clause.
	yng ini adalah contoh sederhana mengunakan query conditions untuk membatasi hasil list view.
	"""
	if not user:    
		user = frappe.session.user
	roles = set(frappe.get_roles(user))
	user_esc = frappe.db.escape(user)
	if user == "Administrator" or "System Manager" in roles:
			return f"(`tabdump_docs`.`alamat`='Tidak Tersedia' AND `tabdump_docs`.`owner`={user_esc})"
	# alamat 'Tidak Tersedia' atau milik user tersebut
	user_esc = frappe.db.escape(user)
	output = f"(`tabdump_docs`.`alamat`='Tidak Tersedia' OR `tabdump_docs`.`owner`={user_esc})"
	return output


def has_permission(doc, user=None):
	"""Akses dokumen individual (detail view) yang konsisten dengan query conditions.

	- Administrator/System Manager: bebas akses.
	- User lain: boleh akses jika alamat == 'Tidak Tersedia' ATAU owner == user.
	"""
	if not user:
		user = frappe.session.user
	roles = set(frappe.get_roles(user))
	if user == "Administrator" or "System Manager" in roles:
		return True
	return (doc.alamat == "Tidak Tersedia") and (doc.owner == user)


class dump_docs(Document):
	
	def before_save(self):
		"""Set default alamat if empty"""
		frappe.logger().info(f"before_save called for {self.name}, alamat={self.alamat}")
		if not self.alamat or self.alamat.strip() == "":
			self.alamat = "Tidak Tersedia"
			frappe.logger().info(f"Set alamat to: {self.alamat}")
	
	def get_title(self):
		"""Custom title format untuk list view"""
		return f"{self.nama} - {self.alamat}"
	
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		nama: DF.Data
		alamat: DF.Data
	# end: auto-generated types
       
	pass
