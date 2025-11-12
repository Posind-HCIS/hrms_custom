import frappe

@frappe.whitelist()
def get_department_count(company):
    return frappe.db.sql("""
        SELECT department, COUNT(*) as count
        FROM `tabEmployee`
        WHERE company = %s AND status = 'Active' AND department IS NOT NULL
        GROUP BY department
        ORDER BY count DESC
    """, company, as_dict=1)

@frappe.whitelist()
def get_gender_distribution(company):
    return frappe.db.sql("""
        SELECT gender, COUNT(*) as count
        FROM `tabEmployee`
        WHERE company = %s AND status = 'Active' AND gender IS NOT NULL
        GROUP BY gender
    """, company, as_dict=1)