frappe.pages['organizational-chart'].on_page_load = function(wrapper) {
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

	// Company selector with custom implementation
	let selected_company = frappe.defaults.get_default("company");
	let company_selector_html = `
		<div style="padding: 10px 15px; border-bottom: 1px solid #d1d8dd;">
			<div style="display: flex; align-items: center; gap: 10px;">
				<label style="margin: 0; font-weight: 600; min-width: 80px;">${__('Company')}:</label>
				<input type="text" class="company-selector-input" 
					   placeholder="${__('Select Company')}" 
					   style="flex: 1; padding: 6px 10px; border: 1px solid #d1d8dd; border-radius: 4px; cursor: pointer;"
					   readonly />
			</div>
		</div>
	`;
	
	page.main.prepend(company_selector_html);
	
	let $company_input = page.main.find('.company-selector-input');
	
	// Set default value
	if (selected_company) {
		$company_input.val(selected_company);
	}
	
	// Click handler to open company selector
	$company_input.on('click', function() {
		let dialog = new frappe.ui.Dialog({
			title: __('Select Company'),
			fields: [
				{
					fieldtype: 'Link',
					fieldname: 'company',
					label: __('Company'),
					options: 'Company',
					default: selected_company,
					reqd: 1
				}
			],
			primary_action_label: __('Select'),
			primary_action: function(values) {
				selected_company = values.company;
				$company_input.val(selected_company);
				loadChart(current_view, selected_company);
				dialog.hide();
			}
		});
		dialog.show();
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
		let view_indicator = $('<div class="view-indicator" style="display: inline-block; margin-left: 10px; padding: 6px 14px; background: #48bb78; color: white; border-radius: 5px; font-size: 13px; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>');
		page.set_title_sub = function(subtitle) {
			view_indicator.text(subtitle);
		};
		
		// Append to page title area
		$('.page-title').append(view_indicator);
		
		// Initial text
		view_indicator.text(__('Viewing: Employees'));
	}, 300);
	
	function updateViewIndicator(view) {
		if (view === 'department') {
			page.set_title_sub(__('Viewing: Departments'));
			$('.view-indicator').css('background', '#667eea');
		} else {
			page.set_title_sub(__('Viewing: Employees'));
			$('.view-indicator').css('background', '#48bb78');
		}
	}

	// Function to load chart
	function loadChart(view, company) {
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
			organizational_chart.company = company;
			
			// Render chart
			organizational_chart.make_svg_markers();
			organizational_chart.setup_hierarchy();
			organizational_chart.render_root_nodes();
			
			// Re-enable company field after chart loads
			setTimeout(() => {
				// Not needed anymore with custom input
			}, 100);
			
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
				loadChart('department', company);
			}, __('View'));

			page.add_inner_button(__('Employees'), function() {
				loadChart('employee', company);
			}, __('View'));
			
			// Add expand/collapse
			page.add_inner_button(__("Expand All"), function () {
				organizational_chart.load_children(organizational_chart.root_node, true);
				organizational_chart.all_nodes_expanded = true;

				page.remove_inner_button(__("Expand All"));
				page.add_inner_button(__("Collapse All"), function () {
					loadChart(view, company);
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
