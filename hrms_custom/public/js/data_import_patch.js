frappe.provide("frappe.core.doctype.data_import.importer");
$.extend(frappe.core.doctype.data_import.importer, {
    Row: class extends frappe.core.doctype.data_import.importer.Row {
        validate_value(value, col) {
            super.validate_value(value, col);
            
            if (this.doctype === "Employee" && col.df && col.df.fieldname === "department") {
                if (value && !frappe.db.exists("Department", value)) {
                    // Hapus semua warning kuning department
                    this.warnings = this.warnings.filter(w => !w.message.includes("missing for Department"));
                    // Paksa jadi error merah
                    this.add_error({
                        row: this.row_number,
                        field: "department",
                        message: `Department '${value}' does not exist. Please create it first.`
                    });
                }
            }
        }
    }
});
console.log("PATCH BERHASIL DIPASANG! Sekarang import Employee → langsung error merah + bisa export!");