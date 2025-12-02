# Test Custom Employee Import

## 🧪 Testing via Python Console

```python
# 1. Import single employee
data = [{
    "employee_name": "Test Employee",
    "first_name": "Test",
    "last_name": "Employee",
    "gender": "Male",
    "date_of_birth": "1990-01-01",
    "date_of_joining": "2024-01-01",
    "department": "IT",
    "designation": "Developer",
    "status": "Active"
}]

from hrms_custom.api.employee_import import import_employees
result = import_employees(data)
print(result)
```

## 📝 Testing via REST API

### 1. Import Employees
```bash
curl -X POST "https://your-site.com/api/method/hrms_custom.api.employee_import.import_employees" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "employee_name": "John Doe",
        "first_name": "John",
        "last_name": "Doe",
        "gender": "Male",
        "date_of_birth": "1990-01-01",
        "date_of_joining": "2024-01-01",
        "department": "IT",
        "designation": "Software Engineer"
      }
    ]
  }'
```

### 2. Validate Before Import
```bash
curl -X POST "https://your-site.com/api/method/hrms_custom.api.employee_import.validate_import_data" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"employee_name": "Test", "date_of_joining": "2024-01-01"}
    ]
  }'
```

### 3. Download Template
```bash
curl -X GET "https://your-site.com/api/method/hrms_custom.api.employee_import.download_template" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  --output employee_template.csv
```

## 💻 Testing via JavaScript (Browser Console)

```javascript
// Import employees
frappe.call({
    method: 'hrms_custom.api.employee_import.import_employees',
    args: {
        data: [
            {
                employee_name: 'Jane Smith',
                first_name: 'Jane',
                last_name: 'Smith',
                gender: 'Female',
                date_of_birth: '1992-05-15',
                date_of_joining: '2024-02-01',
                department: 'HR',
                designation: 'HR Manager'
            }
        ]
    },
    callback: function(r) {
        console.log('Import Result:', r.message);
        
        if (r.message.success > 0) {
            frappe.msgprint(`Successfully imported ${r.message.success} employees`);
        }
        
        if (r.message.errors > 0) {
            console.error('Errors:', r.message.error_details);
        }
    }
});

// Validate data first
frappe.call({
    method: 'hrms_custom.api.employee_import.validate_import_data',
    args: {
        data: [...]
    },
    callback: function(r) {
        console.log('Validation:', r.message);
        
        if (r.message.valid === r.message.total) {
            frappe.msgprint('All data valid! Ready to import.');
        } else {
            frappe.msgprint(`${r.message.invalid} rows have errors`);
        }
    }
});
```

## 📄 Sample CSV File

Create file: `employee_import.csv`

```csv
employee_name,first_name,last_name,gender,date_of_birth,date_of_joining,department,designation,company,status,personal_email,cell_number
John Doe,John,Doe,Male,1990-01-01,2024-01-01,IT,Software Engineer,Your Company,Active,john@example.com,08123456789
Jane Smith,Jane,Smith,Female,1992-05-15,2024-01-15,HR,HR Manager,Your Company,Active,jane@example.com,08987654321
Bob Wilson,Bob,Wilson,Male,1988-03-20,2024-02-01,Finance,Accountant,Your Company,Active,bob@example.com,08555555555
```

## 🔧 Bench Command (Custom)

Create file: `hrms_custom/commands.py`

```python
import click
import frappe
from frappe.commands import pass_context

@click.command('import-employees')
@click.argument('csv-file')
@click.option('--site', help='Site name')
@pass_context
def import_employees_command(context, csv_file, site=None):
    """Import employees from CSV file"""
    
    if not site:
        site = frappe.local.site
    
    frappe.init(site=site)
    frappe.connect()
    
    from hrms_custom.api.employee_import import process_csv_file
    
    # Upload file first
    with open(csv_file, 'rb') as f:
        file_doc = frappe.get_doc({
            'doctype': 'File',
            'file_name': csv_file.split('/')[-1],
            'content': f.read(),
            'is_private': 1
        })
        file_doc.save()
    
    # Process import
    result = process_csv_file(file_doc.file_url)
    
    click.echo(f"Import completed!")
    click.echo(f"Success: {result['success']}")
    click.echo(f"Errors: {result['errors']}")
    
    if result['errors'] > 0:
        click.echo("\nError details:")
        for error in result['error_details']:
            click.echo(f"  Row {error['row']}: {error['error']}")
    
    frappe.db.commit()
    frappe.destroy()

commands = [
    import_employees_command
]
```

Register di `hooks.py`:
```python
# from hrms_custom.commands import commands
```

Usage:
```bash
bench import-employees /path/to/employees.csv --site hrms.locals
```

## ✅ Response Format

### Success Response:
```json
{
  "success": 3,
  "errors": 0,
  "success_details": [
    {
      "row": 1,
      "name": "HR-EMP-00001",
      "employee_name": "John Doe"
    },
    {
      "row": 2,
      "name": "HR-EMP-00002",
      "employee_name": "Jane Smith"
    }
  ],
  "error_details": []
}
```

### Error Response:
```json
{
  "success": 1,
  "errors": 2,
  "success_details": [...],
  "error_details": [
    {
      "row": 2,
      "error": "Employee Jane Smith already exists",
      "data": {"employee_name": "Jane Smith", ...}
    },
    {
      "row": 3,
      "error": "Employee name is required",
      "data": {"first_name": "Bob", ...}
    }
  ]
}
```

## 🚀 Next Steps

1. **Restart bench** after creating files
```bash
bench restart
```

2. **Test API endpoint** via Postman/curl

3. **Create custom page** untuk UI upload (optional)

4. **Add validation rules** sesuai kebutuhan

5. **Setup background jobs** untuk large imports
