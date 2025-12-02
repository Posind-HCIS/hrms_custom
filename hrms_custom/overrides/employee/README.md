# Employee Override Documentation

## Overview
File ini berisi override untuk DocType Employee dari ERPNext ke hrms_custom.

## Struktur File

### Python Controller
- **File**: `hrms_custom/overrides/employee/employee.py`
- **Class**: `Employee` (extends `erpnext.setup.doctype.employee.employee.Employee`)

### JavaScript Files
- **Form Script**: `hrms_custom/public/js/employee.js`
- **List Script**: `hrms_custom/public/js/employee_list.js`

## Konfigurasi di hooks.py

```python
# Extend DocType Class
extend_doctype_class = {
    "Employee": "hrms_custom.overrides.employee.employee.Employee"
}

# Include JavaScript untuk form view
doctype_js = {
    "Employee": "public/js/employee.js"
}

# Include JavaScript untuk list view
doctype_list_js = {
    "Employee": "public/js/employee_list.js"
}
```

## Custom Methods

### Python Methods

#### `custom_validation()`
Custom validation logic untuk Employee.
```python
def custom_validation(self):
    frappe.logger().info(f"Custom validation for Employee: {self.name}")
    # Tambahkan validation logic di sini
```

#### `get_custom_employee_info()`
Mendapatkan informasi custom employee.
```python
def get_custom_employee_info(self):
    return {
        "employee_name": self.employee_name,
        "department": self.department,
        "designation": self.designation,
        "status": self.status
    }
```

### Whitelisted API Methods

#### `get_custom_employee_info(employee)`
**Endpoint**: `/api/method/hrms_custom.overrides.employee.employee.get_custom_employee_info`

**Parameters**:
- `employee`: Employee ID

**Returns**: Employee information dictionary

**Example**:
```javascript
frappe.call({
    method: 'hrms_custom.overrides.employee.employee.get_custom_employee_info',
    args: {
        employee: 'HR-EMP-00001'
    },
    callback: function(r) {
        console.log(r.message);
    }
});
```

#### `custom_employee_method(employee)`
**Endpoint**: `/api/method/hrms_custom.overrides.employee.employee.custom_employee_method`

**Parameters**:
- `employee`: Employee ID

**Returns**: Custom response with employee details

## JavaScript Customization

### Form View (`employee.js`)

**Custom Buttons**:
- **Custom Employee Info**: Menampilkan informasi employee custom
- **Refresh Custom Data**: Refresh data custom

**Field Triggers**:
- `department`: Triggered saat department berubah
- `designation`: Triggered saat designation berubah

**Example**:
```javascript
frappe.ui.form.on('Employee', {
    department: function(frm) {
        if (frm.doc.department) {
            // Custom logic saat department berubah
        }
    }
});
```

### List View (`employee_list.js`)

**Features**:
- Custom indicator berdasarkan status
- Custom formatting untuk fields
- Custom action buttons

## Lifecycle Hooks

### Python Hooks Override

```python
def validate(self):
    super().validate()  # Call parent validation
    self.custom_validation()  # Custom validation

def on_update(self):
    super().on_update()
    # Custom logic after update

def before_save(self):
    # Custom logic before save
    pass
```

## Testing

Setelah setup, restart bench:
```bash
bench restart
```

Clear cache:
```bash
bench clear-cache
```

## Cara Menggunakan

1. **Install app** (jika belum):
   ```bash
   bench --site [site-name] install-app hrms_custom
   ```

2. **Migrate**:
   ```bash
   bench --site [site-name] migrate
   ```

3. **Restart**:
   ```bash
   bench restart
   ```

4. **Clear cache**:
   ```bash
   bench clear-cache
   ```

## Menambahkan Custom Fields

Untuk menambahkan custom fields ke Employee:

1. Buat custom field melalui UI atau via fixture
2. Akses field di Python: `self.custom_field_name`
3. Akses field di JS: `frm.doc.custom_field_name`

## Catatan Penting

1. **Inheritance**: Class `Employee` di hrms_custom meng-inherit dari ERPNext Employee
2. **Method Override**: Selalu panggil `super()` saat override method untuk menjaga logic parent
3. **Whitelisted Methods**: Gunakan decorator `@frappe.whitelist()` untuk method yang bisa dipanggil dari client
4. **JavaScript Priority**: JavaScript di hrms_custom akan di-load setelah JavaScript default Employee

## Troubleshooting

### Override tidak bekerja?
1. Check hooks.py - pastikan `extend_doctype_class` sudah benar
2. Restart bench
3. Clear cache
4. Check browser console untuk JavaScript errors

### Custom method tidak muncul?
1. Pastikan method sudah di-whitelist dengan `@frappe.whitelist()`
2. Check import statement
3. Restart bench

### JavaScript tidak ter-load?
1. Check `doctype_js` di hooks.py
2. Build assets: `bench build`
3. Clear browser cache
4. Check browser console untuk errors
