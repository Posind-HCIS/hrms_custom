import json
import frappe
from frappe import _

@frappe.whitelist()
def get_department_children(parent=None, company=None, department=None, show_self=0, doctype="Department"):
    """ 
    Return departments in the format expected by HRMS HierarchyChart. 
    Robust root detection: computes roots from the full set for the company, 
    not relying on blank parent_department only. 
    
    Args:
        parent: Parent department ID (for expanding children)
        company: Company filter (string or JSON array "[company, department]")
        department: Specific department to show as root (with its children)
        show_self: If 1 and department is set, return the department itself as root node
        doctype: Document type (always "Department" for this function)
    """
    # HACK: Parse company if it's a JSON string array
    if isinstance(company, str) and company.startswith('['):
        try:
            parsed = json.loads(company)
            if isinstance(parsed, list) and len(parsed) >= 2:
                company = parsed[0]
                department = parsed[1] if parsed[1] else department
            elif isinstance(parsed, list) and len(parsed) == 1:
                company = parsed[0]
        except (json.JSONDecodeError, ValueError):
            pass  # Keep company as is if parsing fails
    
    # Company is required - don't return anything if not provided
    if not company or company == "All Companies":
        company = frappe.defaults.get_user_default("company") or frappe.db.get_default("company")
    # If still no company, return empty
    if not company:
        return []
    
    # Convert show_self to int (frappe.whitelist passes strings)
    show_self = int(show_self) if show_self else 0

    all_depts = frappe.get_all(
        "Department",
        filters={
            "company": company,
            "disabled": 0,
            # "department_name": "Sales"
        },
        fields=["name", "department_name", "parent_department", "is_group"],
        order_by="department_name asc",
    )
    

    # Build lookup tables - map parent_department to list of children
    name_set = {d.name for d in all_depts}
    children_by_parent = {}
    for d in all_depts:
        
        # Use actual parent_department value (could be None/""), not normalized to ""
        parent_key = d.parent_department if d.parent_department else None
        children_by_parent.setdefault(parent_key, []).append(d)

    # Detect cycles in the hierarchy
    visited = set()
    rec_stack = set()

    # def dfs(node):
    #     visited.add(node)
    #     rec_stack.add(node)
    #     for child in children_by_parent.get(node, []):
    #         if child.name not in visited:
    #             if dfs(child.name):
    #                 return True
    #         elif child.name in rec_stack:
    #             return True
    #     rec_stack.remove(node)
    #     return False

    # has_cycle_flag = False
    # for d in all_depts:
    #     if d.name not in visited:
    #         if dfs(d.name):
    #             has_cycle_flag = True
    #             break

    # if has_cycle_flag:
    #     frappe.throw(_("Cycle detected in Department hierarchy for company {0}").format(company))

    def make_node(d):
        # Node for HierarchyChart - must match Employee format
        children = children_by_parent.get(d.name, [])
        return frappe._dict({
            "id": d.name,
            "name": d.department_name or d.name,
            "title": "Department",
            "image": "",  # Department doesn't have image
            "expandable": 1 if children else 0,
            "connections": len(children),
            "lft": 0,  # Placeholder values
            "rgt": 0,
            "reports_to": d.parent_department or ""
        })

    nodes = []
    
    # If department filter is set, only show that department tree
    if department:
        # Root request - show the filtered department as root
        if not parent or parent == doctype:
            # Find the specific department
            target_dept = None
            for d in all_depts:
                if d.name == department or d.department_name == department:
                    target_dept = d
                    break
            
            if target_dept:
                nodes.append(make_node(target_dept))
        else:
            # Child request - only return children of the filtered department tree
            # First, get all descendants of the filtered department
            def get_all_descendants(dept_name):
                descendants = set([dept_name])
                children = children_by_parent.get(dept_name, [])
                for child in children:
                    descendants.update(get_all_descendants(child.name))
                return descendants
            
            # Find the filtered department name
            filter_dept_name = None
            for d in all_depts:
                if d.name == department or d.department_name == department:
                    filter_dept_name = d.name
                    break
            
            if filter_dept_name:
                allowed_depts = get_all_descendants(filter_dept_name)
                # Only return children if parent is within allowed tree
                if parent in allowed_depts:
                    for d in children_by_parent.get(parent, []):
                        nodes.append(make_node(d))
    else:
        # No department filter - show all departments
        # Root request - return departments that either have no parent OR parent is outside this company
        if not parent or parent == doctype:
            for d in all_depts:
                # A department is a root if:
                # 1. It has no parent_department (empty/None), OR
                # 2. Its parent_department is not in the same company (not in name_set)
                is_root = not d.parent_department or d.parent_department not in name_set
                if is_root:
                    nodes.append(make_node(d))
            # Fallback: if still empty, return any top-most groups (is_group=1)
            if not nodes:
                for d in all_depts:
                    if d.is_group:
                        nodes.append(make_node(d))
        else:
            # Child request
            for d in children_by_parent.get(parent, []):
                nodes.append(make_node(d))
    
    # Sort nodes by name for stable UI
    nodes.sort(key=lambda x: x["name"])
    return nodes


@frappe.whitelist()
def get_all_department_nodes(company=None):
    """
    Return all departments for expand all functionality.
    Similar to hrms.utils.hierarchy_chart.get_all_nodes but for departments.
    """
    if not company or company == "All Companies":
        company = frappe.defaults.get_user_default("company") or frappe.db.get_default("company")
    
    if not company:
        return []

    all_depts = frappe.get_all(
        "Department",
        filters={
            "company": company,
            "disabled": 0,
        },
        fields=["name", "department_name", "parent_department", "is_group"],
        order_by="department_name asc",
    )

    # Build children lookup
    name_set = {d.name for d in all_depts}
    children_by_parent = {}
    for d in all_depts:
        parent_key = d.parent_department if d.parent_department else None
        children_by_parent.setdefault(parent_key, []).append(d)

    def make_node(d):
        children = children_by_parent.get(d.name, [])
        return frappe._dict({
            "id": d.name,
            "name": d.department_name or d.name,
            "title": "Department",
            "image": "",
            "expandable": 1 if children else 0,
            "connections": len(children),
        })

    # Return all departments as nodes
    nodes = [make_node(d) for d in all_depts]
    return nodes


@frappe.whitelist()
def get_employee_children(parent=None, company=None, exclude_node=None):
    """
    Wrapper for Employee hierarchy that removes avatar/image frame.
    Calls original HRMS get_children but strips image field.
    """
    # Import original HRMS method
    from hrms.hr.page.organizational_chart.organizational_chart import get_children as hrms_get_children
    
    # Call original method
    employees = hrms_get_children(parent=parent, company=company, exclude_node=exclude_node)
    
    # Remove image from each employee node to hide avatar frame
    for emp in employees:
        emp.image = ""
    
    return employees