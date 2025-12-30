# Copyright (c) 2025, me and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class pks(Document):
	pass


@frappe.whitelist()
def update_status_list():
	pks_list = frappe.db.get_all("pks",fields=["name", "tanggal_mulai", "tanggal_selesai"])

	today = frappe.utils.getdate(frappe.utils.nowdate())

	for pks in pks_list:
		if not pks.tanggal_mulai or not pks.tanggal_selesai:
			frappe.db.set_value("pks", pks.name, "status_pks", "Tidak Aktif")	
			continue
	    # ini untuk 1 bulan sebelum, jika 1 bulan sesudah pakai -1
		bulan_peringatan = frappe.utils.getdate(frappe.utils.add_months(pks.tanggal_selesai, 1))
		
		if today > pks.tanggal_selesai:
			frappe.db.set_value("pks", pks.name, "status_pks", "Tidak Aktif")
		elif bulan_peringatan and bulan_peringatan > today and today > pks.tanggal_mulai and today <= pks.tanggal_selesai:
			frappe.db.set_value("pks", pks.name, "status_pks", "Masa Tenggang")
		else:
			frappe.db.set_value("pks", pks.name, "status_pks", "Aktif")