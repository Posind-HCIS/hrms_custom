import frappe

def update_dump_docs_fields():
    """Update custom fields for dump_docs doctype"""
    
    # Update alamat field
    if frappe.db.exists("Custom Field", "dump_docs-alamat"):
        doc = frappe.get_doc("Custom Field", "dump_docs-alamat")
        doc.filterable = 1
        doc.searchable = 1
        doc.save()
        frappe.db.commit()
    
    # Update nama field if exists
    if frappe.db.exists("Custom Field", "dump_docs-nama"):
        doc = frappe.get_doc("Custom Field", "dump_docs-nama")
        doc.filterable = 1
        doc.searchable = 1
        doc.save()
        frappe.db.commit()
