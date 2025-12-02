// Copyright (c) 2025, me and contributors
// For license information, please see license.txt

// Custom Employee Form Script
frappe.ui.form.on('Employee', {
	refresh: function(frm) {
		// Custom behavior saat form refresh
		console.log('Custom Employee form loaded:', frm.doc.name);
		
		// Tambahkan custom button
		if (!frm.is_new()) {
			frm.add_custom_button(__('Custom Employee Info'), function() {
				frappe.call({
					method: 'hrms_custom.overrides.employee.employee.get_custom_employee_info',
					args: {
						employee: frm.doc.name
					},
					callback: function(r) {
						if (r.message) {
							frappe.msgprint({
								title: __('Employee Information'),
								message: `
									<b>Name:</b> ${r.message.employee_name || 'N/A'}<br>
									<b>Department:</b> ${r.message.department || 'N/A'}<br>
									<b>Designation:</b> ${r.message.designation || 'N/A'}<br>
									<b>Status:</b> ${r.message.status || 'N/A'}
								`,
								indicator: 'blue'
							});
						}
					}
				});
			});
		}
		
		// Contoh: Custom button untuk refresh data
		frm.add_custom_button(__('Refresh Custom Data'), function() {
			frappe.show_alert({
				message: __('Custom data refreshed!'),
				indicator: 'green'
			});
		}, __('Actions'));
	},
	
	// Custom behavior saat field department berubah
	department: function(frm) {
		if (frm.doc.department) {
			console.log('Department changed to:', frm.doc.department);
			// Tambahkan custom logic, misalnya auto-populate designation
			// atau validasi tertentu
		}
	},
	
	// Custom behavior saat field designation berubah
	designation: function(frm) {
		if (frm.doc.designation) {
			console.log('Designation changed to:', frm.doc.designation);
			// Tambahkan custom logic di sini
		}
	},
	
	// Custom validation before save
	validate: function(frm) {
		// Tambahkan custom validation
		// Contoh:
		// if (frm.doc.custom_field && !frm.doc.department) {
		// 	frappe.msgprint(__('Please select a department'));
		// 	frappe.validated = false;
		// }
	},
	
	// Custom behavior sebelum submit
	before_save: function(frm) {
		console.log('Employee about to be saved:', frm.doc.employee_name);
	}
});
