# Copyright (c) 2025, me and contributors
# For license information, please see license.txt

import frappe
from erpnext.setup.doctype.employee.employee import Employee as BaseEmployee


class Employee(BaseEmployee):
	"""
	Custom Employee class yang override dari ERPNext.
	Tambahkan custom logic di sini.
	"""
	
	def validate(self):
		"""
		Override validate method.
		Panggil parent validate dulu, lalu tambahkan custom validation.
		"""
		# Panggil validate dari parent class (ERPNext Employee)
		super().validate()
		
		# Tambahkan custom validation di sini
		self.custom_validation()
	
	def custom_validation(self):
		"""
		Custom validation logic untuk Employee.
		Contoh: validasi custom field, business logic khusus, dll.
		"""
		# Contoh: Log saat employee di-save
		frappe.logger().info(f"Custom validation for Employee: {self.name}")
		
		# Validasi department exists
		if self.department:
			if not frappe.db.exists("Department", self.department):
				frappe.throw(
					title=frappe._("Invalid Department"),
					msg=frappe._(
						"Row {0}: Department '<b>{1}</b>' does not exist in the system. "
						"Please create the department first or correct the name in the import file."
					).format(getattr(self, 'idx', ''), self.department)
				)
		
		# Tambahkan custom validation logic di sini
		# Contoh:
		# if self.custom_field:
		# 	frappe.throw("Custom field validation message")
	
	def on_update(self):
		"""
		Override on_update method.
		Method ini dipanggil setelah employee di-update.
		"""
		super().on_update()
		
		# Tambahkan custom logic saat update
		frappe.logger().info(f"Employee {self.name} updated - Custom logic executed")
	
	def before_save(self):
		"""
		Method yang dipanggil sebelum employee di-save.
		"""
		# Tambahkan custom logic sebelum save
		frappe.logger().info(f"Before saving Employee: {self.name}")
	
	# Tambahkan custom methods di sini
	def get_custom_employee_info(self):
		"""
		Contoh custom method untuk mendapatkan informasi employee.
		"""
		return {
			"employee_name": self.employee_name,
			"department": self.department,
			"designation": self.designation,
			"status": self.status
		}


# Whitelisted methods yang bisa dipanggil dari client-side
@frappe.whitelist()
def get_custom_employee_info(employee):
	"""
	Get custom employee information.
	Bisa dipanggil dari JavaScript dengan frappe.call()
	
	Args:
		employee: Employee ID
	
	Returns:
		dict: Employee information
	"""
	emp = frappe.get_doc("Employee", employee)
	return emp.get_custom_employee_info()


@frappe.whitelist()
def custom_employee_method(employee):
	"""
	Contoh custom method untuk Employee.
	Tambahkan custom business logic di sini.
	
	Args:   
		employee: Employee ID
	
	Returns:
		dict: Response message
	"""
	emp_doc = frappe.get_doc("Employee", employee)
	
	return {
		"message": f"Custom method called for {emp_doc.employee_name}",
		"employee_id": employee,
		"department": emp_doc.department,
		"status": emp_doc.status
	}
