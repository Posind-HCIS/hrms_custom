// Copyright (c) 2025, me and contributors
// For license information, please see license.txt

// Custom Employee List View Script
frappe.listview_settings['Employee'] = {
	add_fields: ["status", "department", "designation", "employee_name"],
	
	onload: function(listview) {
		// Custom logic saat list view di-load
		console.log('Custom Employee list view loaded');
	},
	
	// Custom button di list view
	button: {
		show: function(doc) {
			return doc.status === "Active";
		},
		get_label: function() {
			return __('Custom Action');
		},
		get_description: function(doc) {
			return __('Perform custom action for {0}', [doc.employee_name]);
		},
		action: function(doc) {
			frappe.msgprint(__('Custom action for employee: {0}', [doc.employee_name]));
		}
	},
	
	// Custom formatting untuk list items
	formatters: {
		status: function(value) {
			// Custom color coding untuk status
			if (value === "Active") {
				return `<span class="indicator green">${value}</span>`;
			} else if (value === "Left") {
				return `<span class="indicator red">${value}</span>`;
			} else {
				return `<span class="indicator orange">${value}</span>`;
			}
		}
	},
	
	// Custom menu actions
	get_indicator: function(doc) {
		// Show custom indicator based on status
		if (doc.status === "Active") {
			return [__("Active"), "green", "status,=,Active"];
		} else if (doc.status === "Left") {
			return [__("Left"), "red", "status,=,Left"];
		} else if (doc.status === "Suspended") {
			return [__("Suspended"), "orange", "status,=,Suspended"];
		} else {
			return [__("Inactive"), "gray", "status,=,Inactive"];
		}
	}
};
