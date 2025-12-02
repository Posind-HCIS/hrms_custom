# Employee Override - Custom Fixtures Example

## Cara Export Custom Fields untuk Employee

Jika Anda menambahkan custom fields ke Employee DocType, Anda bisa export dan import menggunakan fixtures.

### 1. Tambahkan ke hooks.py

```python
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            [
                "dt", "=", "Employee"
            ]
        ]
    },
    {
        "dt": "Property Setter",
        "filters": [
            [
                "doc_type", "=", "Employee"
            ]
        ]
    }
]
```

### 2. Export fixtures

```bash
bench --site [site-name] export-fixtures
```

### 3. File yang di-generate

Custom fields akan di-export ke folder:
- `hrms_custom/fixtures/custom_field.json`
- `hrms_custom/fixtures/property_setter.json`

### 4. Import di site baru

Saat install app di site baru, fixtures akan otomatis ter-import.

## Contoh Custom Field untuk Employee

```json
{
    "doctype": "Custom Field",
    "dt": "Employee",
    "label": "Custom Employee Code",
    "fieldname": "custom_employee_code",
    "fieldtype": "Data",
    "insert_after": "employee_number",
    "reqd": 0
}
```

## Cara Membuat Custom Field via Code

```python
import frappe

def create_custom_field():
    if not frappe.db.exists("Custom Field", {"dt": "Employee", "fieldname": "custom_employee_code"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Employee",
            "label": "Custom Employee Code",
            "fieldname": "custom_employee_code",
            "fieldtype": "Data",
            "insert_after": "employee_number",
            "reqd": 0
        }).insert()
```

Panggil function ini di `after_install` hook atau via patch.
