# Employee Override - Quick Reference

## 🚀 Quick Start

### 1. Setup
```bash
# Restart bench
bench restart

# Clear cache
bench clear-cache

# Build if needed
bench build --app hrms_custom
```

### 2. Verify Override Active
Buka Employee form dan check console browser untuk message:
```
Custom Employee form loaded: [Employee ID]
```

## 📝 Common Use Cases

### Override validate()
```python
def validate(self):
    super().validate()
    
    # Custom validation
    if self.custom_field and not self.department:
        frappe.throw("Department required when custom_field is set")
```

### Add custom method
```python
@frappe.whitelist()
def my_custom_method(employee):
    emp = frappe.get_doc("Employee", employee)
    # Your logic here
    return {"status": "success"}
```

### Call from JavaScript
```javascript
frappe.call({
    method: 'hrms_custom.overrides.employee.employee.my_custom_method',
    args: { employee: frm.doc.name },
    callback: function(r) {
        console.log(r.message);
    }
});
```

### Add custom button
```javascript
frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        frm.add_custom_button('My Button', function() {
            // Your code
        });
    }
});
```

### Auto-fill field
```javascript
frappe.ui.form.on('Employee', {
    department: function(frm) {
        if (frm.doc.department) {
            // Auto-fill logic
            frm.set_value('custom_field', 'some_value');
        }
    }
});
```

## 🔧 Troubleshooting Commands

```bash
# Restart bench
bench restart

# Clear all cache
bench clear-cache

# Clear browser cache
bench --site [site-name] clear-website-cache

# Rebuild
bench build --app hrms_custom

# Check logs
tail -f logs/frappe.log

# Check if override is loaded
bench console
>>> from hrms_custom.overrides.employee.employee import Employee
>>> Employee
```

## 📍 File Locations

```
hrms_custom/
├── overrides/
│   └── employee/
│       ├── __init__.py
│       ├── employee.py          # Python controller
│       ├── test_employee_override.py
│       ├── README.md
│       └── FIXTURES.md
├── public/
│   └── js/
│       ├── employee.js          # Form script
│       └── employee_list.js     # List script
└── hooks.py                     # Configuration
```

## 🎯 Key Configurations in hooks.py

```python
# Python class override
extend_doctype_class = {
    "Employee": "hrms_custom.overrides.employee.employee.Employee"
}

# JavaScript form override
doctype_js = {
    "Employee": "public/js/employee.js"
}

# JavaScript list override
doctype_list_js = {
    "Employee": "public/js/employee_list.js"
}
```

## 📚 Testing

```bash
# Run tests
bench --site [site-name] run-tests --app hrms_custom

# Run specific test
bench --site [site-name] run-tests --app hrms_custom --module hrms_custom.overrides.employee.test_employee_override
```

## ⚡ Development Workflow

1. Edit Python file: `employee.py`
2. Restart: `bench restart`
3. Edit JavaScript: `employee.js`
4. Build: `bench build --app hrms_custom`
5. Hard refresh browser: `Ctrl+Shift+R`
6. Test changes

## 🐛 Common Issues

### Override not working?
✅ Check `extend_doctype_class` in hooks.py
✅ Restart bench
✅ Clear cache

### JS not loading?
✅ Check `doctype_js` in hooks.py
✅ Run `bench build`
✅ Clear browser cache

### Method not found?
✅ Add `@frappe.whitelist()` decorator
✅ Check import path
✅ Restart bench
