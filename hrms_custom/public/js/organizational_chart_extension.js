frappe.pages['organizational-chart'].on_page_load = function (wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Organizational Chart',
		single_column: true
	});

	let page = wrapper.page;
	let organizational_chart;
	let current_view = 'employee'; // default view

	// Setup page styling
	page.main.addClass("frappe-card");
	page.main.css({
		"min-height": "300px",
		"max-height": "700px",
		overflow: "auto",
		position: "relative"
	});

	// Custom company selector
	let selected_company = frappe.defaults.get_default("company");
	let selected_department = frappe.defaults.get_default("department");
	format = (selected_company != null ? selected_company : '') + (selected_department != null ? ' - ' + selected_department : '');

	let company_selector_html = `
		<div class="custom-company-selector" style="padding: 10px 15px; border-bottom: 1px solid #d1d8dd; background: #f9fafb; position: relative; z-index: 1000;">
			<div style="display: flex; align-items: center; gap: 10px;">
				<strong style="font-size: 14px; color: #1f2937;">Company:</strong>
				<div class="company-display" style="flex: 1; padding: 7px 12px; background: white; border: 1px solid #d1d8dd; border-radius: 6px; cursor: pointer; display: flex; align-items: center; justify-content: space-between; transition: all 0.2s; position: relative; z-index: 1001;">
					<span class="company-name" style="color: #374151; font-size: 14px;">${format || 'Click to select company'}</span>
					<svg style="width: 16px; height: 16px; color: #6b7280;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
					</svg>
				</div>
			</div>
		</div>
	`;

	page.main.prepend(company_selector_html);

	// Click handler - menggunakan event delegation pada page.main
	page.main.on('click', '.company-display', function () {
		let dialog = new frappe.ui.Dialog({
			title: __('Select Company'),
			fields: [{
					fieldtype: 'Link',
					fieldname: 'company',
					label: __('Company'),
					options: 'Company',
					default: selected_company,
					reqd: 1,
					onchange: function () {
						// Clear department field when company changes
						dialog.set_value('department', '');
						// Refresh department field to apply new filter
						if (dialog.fields_dict.department) {
							dialog.fields_dict.department.refresh();
						}
					}
				},
				{
					fieldtype: 'Link',
					fieldname: 'department',
					label: __('Department'),
					options: 'Department',
					// depends_on: 'eval:doc.company',
					get_query: function () {
						let company = dialog.get_value('company');
						if (company) {
							return {
								filters: {
									'company': company
								}
							};
						}
						return {};
					}
				}
			],
			primary_action_label: __('Select'),
			primary_action: function (values) {
				selected_company = values.company;
				selected_department = values.department;
				$('.company-name').text(selected_company + (selected_department ? ' - ' + selected_department : ''));
				loadChart(current_view, selected_company, selected_department);
				dialog.hide();
			}
		});
		dialog.show();
	});
	
	// Hover effect - menggunakan event delegation pada page.main
	page.main.on('mouseenter', '.company-display', function() {
		$(this).css({
			'border-color': '#3b82f6',
			'box-shadow': '0 0 0 3px rgba(59, 130, 246, 0.1)'
		});
	}).on('mouseleave', '.company-display', function() {
		$(this).css({
			'border-color': '#d1d8dd',
			'box-shadow': 'none'
		});
	});

	// View toggle buttons in toolbar
	page.add_inner_button(__('Departments'), function() {
		current_view = 'department';
		if (selected_company) {
			loadChart('department', selected_company);
		} else {
			frappe.msgprint(__('Please select a company first'));
		}
	}, __('View'));

	page.add_inner_button(__('Employees'), function() {
		current_view = 'employee';
		if (selected_company) {
			loadChart('employee', selected_company);
		} else {
			frappe.msgprint(__('Please select a company first'));
		}
	}, __('View'));
	
	// Add view indicator label after page loads
	setTimeout(() => {
		//let view_indicator = $('<div class="view-indicator" style="display: inline-block; margin-left: 10px; padding: 6px 14px; background: #48bb78; color: white; border-radius: 5px; font-size: 13px; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>');
		let view_indicator = $('<div class="view-indicator" style="font-weight:bold;"></div>');
		
        page.set_title_sub = function(subtitle) {
			view_indicator.text(subtitle);
		};
		
		// Append to page title area
		$('.title-area>div>.flex').append(view_indicator);
		
		// Initial text
        view_indicator.text(__('| Employees'));
	}, 300);
	
	function updateViewIndicator(view) {
		if (view === 'department') {
			page.set_title_sub(__('| Departments'));    
			// $('.view-indicator').css('background', '#667eea');
		} else {
			page.set_title_sub(__('| Employees'));
			// $('.view-indicator').css('background', '#48bb78');
		}
	}

	// Function to load chart
	function loadChart(view, company, department) {
		// Update view indicator
		updateViewIndicator(view);
		
		frappe.require("hierarchy-chart.bundle.js", () => {
			// Clear existing chart
			page.main.find('#hierarchy-chart-wrapper').remove();
			
			let method;
			let doctype;
			
			if (view === 'department') {
				method = 'hrms_custom.api.get_department_children';
				doctype = 'Department';
			} else {
				method = 'hrms_custom.api.get_employee_children';
				doctype = 'Employee';
			}
			
			// Create chart
			if (frappe.is_mobile()) {
				organizational_chart = new hrms.HierarchyChartMobile(doctype, wrapper, method);
			} else {
				organizational_chart = new hrms.HierarchyChart(doctype, wrapper, method);
			}
			
			// Override company to use selected one
			organizational_chart.company = [company, department];
			
			// Render chart
			organizational_chart.make_svg_markers();
			organizational_chart.setup_hierarchy();
			organizational_chart.render_root_nodes();
			
			// Override load_children to trigger event after loading
			let original_load_children = organizational_chart.load_children.bind(organizational_chart);
			organizational_chart.load_children = function(node, deep = false) {
				original_load_children(node, deep);
				setTimeout(() => {
					$(document).trigger('hierarchy-children-loaded');
				}, 300);
			};
			
			// Setup click handlers for nodes
			setTimeout(() => {
				setupNodeClickHandlers(organizational_chart, doctype);
			}, 500);
			
			// Setup Export and Expand buttons
			page.clear_inner_toolbar();
			
			// Re-add view buttons
			page.add_inner_button(__('Departments'), function() {
				loadChart('department', company, department);
			}, __('View'));

			page.add_inner_button(__('Employees'), function() {
				loadChart('employee', company, department);
			}, __('View'));
			
			// Add expand/collapse
			page.add_inner_button(__("Expand All"), function () {
				organizational_chart.load_children(organizational_chart.root_node, true);
				organizational_chart.all_nodes_expanded = true;

				page.remove_inner_button(__("Expand All"));
				page.add_inner_button(__("Collapse All"), function () {
					loadChart(view, company, department);
					organizational_chart.all_nodes_expanded = false;
					page.remove_inner_button(__("Collapse All"));
				});
			});

			// Add export
			page.add_inner_button(__("Export"), function () {
				organizational_chart.export_chart();
			});
		});
	}

	// Auto-trigger on load
	setTimeout(() => {
		if (selected_company) {
			loadChart(current_view, selected_company);
		}
		updateViewIndicator(current_view); // Set initial indicator
	}, 100);

	frappe.breadcrumbs.add("HR");
};

// Setup node click handlers
function setupNodeClickHandlers(organizational_chart, doctype) {
	$('.node-card').off('dblclick').each(function() {
		let $card = $(this);
		let node_id = $card.attr('id');
		
		if (!node_id) return;
		
		// Double click - open detail form
		$card.on('dblclick', function(e) {
			e.preventDefault();
			e.stopPropagation();
			frappe.set_route('Form', doctype, node_id);
		});
	});
	
	// Re-attach expand/collapse handlers after children load
	$(document).off('hierarchy-children-loaded').on('hierarchy-children-loaded', function() {
		setTimeout(() => {
			setupNodeClickHandlers(organizational_chart, doctype);
		}, 100);
	});
}
