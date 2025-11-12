// Custom List View untuk dump_docs
frappe.listview_settings["dump_docs"] = {
	add_fields: ["nama", "alamat"],
	hide_name_column: false,
	order_by: "creation desc"

    
};
