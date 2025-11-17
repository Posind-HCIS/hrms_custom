import frappe , requests

# ini buat get api employee test 
@frappe.whitelist()
def get_employee():
    return {
        "message": "Data retrieved successfully",
        "data": frappe.db.get_list('Employee',
                                   fields=['*'],
            limit=10
        )
    }

@frappe.whitelist()
def find_employee_by_name(name):
    employee = frappe.db.get_list('Employee',fields=['*'], filters={'employee_name': name}, limit=1)
    if employee:
        return employee[0]
    else:
        return None

@frappe.whitelist(methods=['POST'])
def create_employee(employee_name, company, status):  
    # cek apakah request nya sudah post
    if frappe.request.method != 'POST':
        frappe.throw("Invalid request method. Please use POST.")

    new_employee = frappe.get_doc({
        'doctype': 'Employee',
        'employee_name': employee_name,
        'first_name': employee_name.split()[0],
        'company': company, 
        'status': status,
        'gender': 'Male',  # contoh tambahan field   
        'date_of_birth': '1990-01-01',  # contoh tambahan field
        'date_of_joining': '2023-01-01'  # contoh tambahan field
    })
    
    new_employee.insert()

    return {
        "message": "Employee created successfully",
        "employee": new_employee.as_dict()
    }

@frappe.whitelist(methods=['POST'])
def update_employee(employee_name, status):
    if frappe.request.method != 'POST':
        frappe.throw("Invalid request method. Please use POST.")

    employee = frappe.db.get_list('Employee', fields=['*'], filters={'employee_name': employee_name}, limit=1)
    if not employee:
        return {"message": "Employee not found"}
    
    

    emp_doc = frappe.get_doc('Employee', employee[0]['name'])
    emp_doc.status = status
    emp_doc.save()

    return {
        "message": "Employee updated successfully",
        "employee": emp_doc.as_dict()
    }

@frappe.whitelist(methods=['DELETE'])
def delete_employee(employee_name):
    if frappe.request.method != 'DELETE':
        frappe.throw("Invalid request method. Please use DELETE.")
    employee = frappe.db.get_list('Employee', fields=['*'], filters={'employee_name': employee_name}, limit=1)
    if not employee:
        return {"message": "Employee not found"}

    emp_doc = frappe.get_doc('Employee', employee[0]['name'])
    emp_doc.delete()

    return {"message": "Employee deleted successfully"}