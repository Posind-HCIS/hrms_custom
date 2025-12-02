// Copyright (c) 2025, me and contributors
// For license information, please see license.txt

// Custom Employee form behavior
frappe.ui.form.on('Employee', {
	refresh: function(frm) {
		// Tambahkan custom button atau custom behavior di sini
		
		// Contoh: Tambahkan custom button
		if (!frm.is_new()) {
			frm.add_custom_button(__('Custom Action'), function() {
				frappe.msgprint(__('Custom action triggered!'));
				
				// Contoh: Call custom whitelisted method
				frappe.call({
					method: 'hrms_custom.overrides.employee.employee.custom_employee_method',
					args: {
						employee: frm.doc.name
					},
					callback: function(r) {
						if (r.message) {
							frappe.msgprint(__('Response: ') + JSON.stringify(r.message));
						}
					}
				});
			});
		}
		
		// Custom logic saat form refresh
		console.log('Custom Employee form loaded for:', frm.doc.name);
	},
	
	// Custom behavior saat field berubah
	department: function(frm) {
		// Contoh: Auto-fill atau validasi saat department berubah
		if (frm.doc.department) {
			console.log('Department changed to:', frm.doc.department);
			// Tambahkan custom logic di sini
		}
	},
	
	// Contoh: Custom behavior saat designation berubah
	designation: function(frm) {
		if (frm.doc.designation) {
			console.log('Designation changed to:', frm.doc.designation);
			// Tambahkan custom logic di sini
		}
	},
	
	// Custom validation sebelum save
	validate: function(frm) {
		// Tambahkan custom validation di sini
		// Contoh:
		// if (frm.doc.custom_field && frm.doc.custom_field < 0) {
		// 	frappe.msgprint(__('Custom field cannot be negative'));
		// 	validated = false;
		// }
	}
});
