// Copyright (c) 2025, me and contributors
// For license information, please see license.txt

// frappe.ui.form.on("pks", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("pks", {
    validate: (frm) => {
        if (frm.doc.tanggal_mulai && frm.doc.tanggal_selesai) {
            if (frm.doc.tanggal_mulai > frm.doc.tanggal_selesai) {
                frappe.msgprint("Tanggal Mulai tidak boleh lebih besar dari Tanggal Selesai");
                frm.doc.tanggal_selesai = "";
                frappe.validated = false;

            }
        }
    },
    refresh: (frm) => {
        frm.trigger("update_status");
    },
    update_status: (frm) => {
        if (!frm.doc.tanggal_selesai || !frm.doc.tanggal_mulai) {
            frm.set_value("status_pks", "Tidak Aktif");
            return;
        }
        let today = frappe.datetime.get_today();
        let Mulai = frm.doc.tanggal_mulai;
        let Selesai = frm.doc.tanggal_selesai;

        let status = "Tidak Aktif";
        // cek 1 bulan sebelum selesai
        let one_month_before_end = frappe.datetime.add_months(Selesai, -1);

        if (one_month_before_end <= today && today <= Selesai) {
            status = "Masa Tenggang";
        } else if (Mulai <= today && today < one_month_before_end) {
            status = "Aktif";
        }
        frm.set_value("status_pks", status);
    }
});