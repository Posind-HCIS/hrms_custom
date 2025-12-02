frappe.listview_settings["Employee"] = {
    hide_name_column: true,  // Sembunyikan kolom nama
    add_fields: [
        "employee_name",   // Full Name → kolom ke-2
        "department",      // kolom ke-3
        "designation",     // kolom ke-4
        "status"           // kolom ke-5 (gak bisa di-hide, tapi bisa diurutkan)
    ],
    // Indicator tetap jalan
    get_indicator: function(doc) {
        if (doc.status === "Active") return ["Active", "green", "status,=,Active"];
        if (doc.status === "Left") return ["Left", "gray", "status,=,Left"];
        return ["Inactive", "red", "status,=,Inactive"];
    }
};