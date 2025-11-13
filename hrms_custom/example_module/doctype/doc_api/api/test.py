# File: apps/myapp/myapp/api.py  (atau di controller DocType)

from routex import routex_whitelist
import frappe

@routex_whitelist("get-users")
def get_users():
    users = frappe.get_list("User", fields=["name", "email"])
    return {
        "users": users,
        "total": len(users)
    }