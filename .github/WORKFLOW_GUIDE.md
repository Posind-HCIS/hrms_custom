# GitHub Workflow Documentation - HRMS Custom

## 📁 Struktur File yang Dibuat

```
.github/
├── workflows/
│   ├── ci.yml              # Main CI/CD pipeline
│   └── linters.yml         # Code quality checks
├── ISSUE_TEMPLATE/
│   ├── bug_report.md       # Template untuk bug report
│   └── feature_request.md  # Template untuk feature request
├── PULL_REQUEST_TEMPLATE.md # Template untuk PR
└── dependabot.yml          # Auto-update dependencies
```

---

## 🔄 Workflow Overview

### 1. **CI Workflow** (`ci.yml`)
Berjalan otomatis saat:
- Push ke branch `main` atau `develop`
- Pull Request ke `main` atau `develop`
- Manual trigger via GitHub UI

**Jobs yang dijalankan:**

#### 🔍 **Linters** (Job 1)
- Setup Python 3.11
- Cache pre-commit hooks
- Run semua pre-commit checks:
  - Trailing whitespace
  - Merge conflicts
  - Python AST validation
  - JSON/YAML/TOML validation
  - Ruff linting & formatting
  - Prettier (JS/Vue/SCSS)
  - ESLint (JavaScript)

#### 🧪 **Unit Tests** (Job 2)
- Setup MariaDB 10.6
- Install Frappe Bench
- Initialize Frappe v15 bench
- Install HRMS Custom app
- Install HRMS dependency
- Create test site
- Run tests with coverage
- Upload coverage ke Codecov

#### 📦 **Build Check** (Job 3)
- Build Python package
- Validate package dengan twine

---

### 2. **Linters Workflow** (`linters.yml`)
Workflow terpisah khusus untuk code quality.

**Jobs:**
- **Pre-commit Checks**: Semua validasi pre-commit
- **Ruff Check**: Python linting & formatting

---

## 🚀 Cara Menggunakan

### **Setup Awal**

1. **Install Pre-commit di lokal:**
```bash
cd /home/rafieaydin/frappe_framework/bench/apps/hrms_custom
pip install pre-commit
pre-commit install
```

2. **Commit file workflow:**
```bash
git add .github/
git commit -m "ci: add GitHub Actions workflows and templates"
git push origin main
```

3. **Enable GitHub Actions:**
   - Buka: https://github.com/Posind-HCIS/hrms_custom/actions
   - Klik "I understand my workflows, go ahead and enable them"

---

## 📝 Development Workflow

### **Standard Flow:**

```bash
# 1. Buat branch baru
git checkout -b feat/nama-fitur-baru

# 2. Coding...
# Pre-commit akan auto-run saat commit
git add .
git commit -m "feat: tambah fitur X"

# 3. Push ke GitHub
git push origin feat/nama-fitur-baru

# 4. Buat PR di GitHub
# - Template PR akan otomatis muncul
# - CI akan berjalan otomatis
# - Review checklist di template

# 5. Merge setelah:
# - ✅ CI passed
# - ✅ Code review approved
# - ✅ Conflicts resolved
```

---

## 🏷️ Commit Convention

Gunakan format: `<type>: <description>`

**Types:**
- `feat:` - Fitur baru
- `fix:` - Bug fix
- `docs:` - Dokumentasi
- `style:` - Formatting (tidak mengubah logic)
- `refactor:` - Refactoring code
- `perf:` - Performance improvement
- `test:` - Menambah tests
- `chore:` - Maintenance tasks
- `ci:` - CI/CD changes

**Contoh:**
```bash
git commit -m "feat: add employee attendance override feature"
git commit -m "fix: resolve payroll calculation bug"
git commit -m "docs: update installation guide"
```

---

## 🐛 Issue Templates

### **Bug Report**
Gunakan saat menemukan bug:
1. Buka: https://github.com/Posind-HCIS/hrms_custom/issues/new
2. Pilih "Bug Report"
3. Isi template dengan lengkap

### **Feature Request**
Gunakan saat ingin request fitur baru:
1. Buka: https://github.com/Posind-HCIS/hrms_custom/issues/new
2. Pilih "Feature Request"
3. Jelaskan use case & benefit

---

## 🔧 Troubleshooting

### **Pre-commit Failed**
```bash
# Lihat error detail
pre-commit run --all-files --verbose

# Fix specific hook
pre-commit run ruff --all-files

# Skip pre-commit (tidak recommended)
git commit --no-verify -m "message"
```

### **CI Failed di GitHub**
1. Cek logs di GitHub Actions
2. Reproduce di lokal:
   ```bash
   pre-commit run --all-files
   ```
3. Fix error & push ulang

### **Update Pre-commit Hooks**
```bash
pre-commit autoupdate
git add .pre-commit-config.yaml
git commit -m "chore: update pre-commit hooks"
```

---

## 📊 Monitoring

### **GitHub Actions**
- Dashboard: https://github.com/Posind-HCIS/hrms_custom/actions
- Lihat workflow runs
- Download artifacts (coverage reports)

### **Dependabot**
- Auto-update dependencies setiap minggu
- Create PR otomatis untuk updates
- Review & merge sesuai kebutuhan

---

## 🔐 Secrets (Jika Diperlukan)

Jika butuh Codecov atau secrets lain:

1. Buka: https://github.com/Posind-HCIS/hrms_custom/settings/secrets/actions
2. Klik "New repository secret"
3. Tambah:
   - `CODECOV_TOKEN` - untuk coverage reports

---

## 📚 Resources

- **Pre-commit**: https://pre-commit.com/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Ruff**: https://docs.astral.sh/ruff/
- **Frappe Testing**: https://frappeframework.com/docs/user/en/testing

---

## ✅ Next Steps

1. ✅ File sudah dibuat
2. ⏳ Commit & push ke GitHub
3. ⏳ Enable GitHub Actions
4. ⏳ Setup Codecov (optional)
5. ⏳ Test workflow dengan membuat PR

---

**Dibuat pada:** 27 November 2025  
**Maintainer:** Posind-HCIS Team
