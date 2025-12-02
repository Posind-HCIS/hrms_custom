# 🚀 Quick Start - SonarCloud Setup

## ⚡ Langkah Cepat (5 Menit)

### 1️⃣ **Setup SonarCloud**
1. Buka: https://sonarcloud.io
2. Login dengan GitHub (Posind-HCIS)
3. Klik **"+"** → **"Analyze new project"**
4. Pilih: **`Posind-HCIS/hrms_custom`**
5. Klik **"Set Up"**
6. **⚠️ PENTING - Disable Automatic Analysis:**
   - Setelah project dibuat, klik **Administration** tab
   - Pilih **Analysis Method** (sidebar)
   - Toggle **OFF** untuk "Automatic Analysis"
   - Pilih **"GitHub Actions"** sebagai method
   - Klik **Save**

### 2️⃣ **Generate Token**
1. Di SonarCloud, klik icon user → **My Account** → **Security**
2. Generate Tokens:
   - Name: `GitHub Actions HRMS Custom`
   - Type: `Global Analysis Token`  
   - Expires: `No expiration`
3. **COPY TOKEN** (hanya muncul sekali!)

### 3️⃣ **Add Token ke GitHub**
1. Buka: https://github.com/Posind-HCIS/hrms_custom/settings/secrets/actions
2. Klik **"New repository secret"**
3. Isi:
   - **Name:** `SONAR_TOKEN`
   - **Value:** `<paste token dari step 2>`
4. Klik **"Add secret"**

### 4️⃣ **Commit & Push**
```bash
cd /home/rafieaydin/frappe_framework/bench/apps/hrms_custom

# Add all changes
git add .

# Commit
git commit -m "ci: setup SonarCloud workflow for code quality analysis"

# Push
git push origin main
```

### 5️⃣ **Verifikasi**
1. Check workflow: https://github.com/Posind-HCIS/hrms_custom/actions
2. Lihat hasil: https://sonarcloud.io/project/overview?id=Posind-HCIS_hrms_custom

---

## 📊 Apa yang Dianalisis?

SonarCloud otomatis mengecek:
- ✅ **Bugs** - Potensi error di code
- ✅ **Vulnerabilities** - Security issues
- ✅ **Code Smells** - Maintainability issues
- ✅ **Coverage** - Test coverage percentage
- ✅ **Duplications** - Duplicate code
- ✅ **Security Hotspots** - Code yang perlu security review

---

## 🎯 Yang Sudah Dikonfigurasi

### ✅ File yang Ada:
- `.github/workflows/sonarcloud.yml` - Main workflow
- `sonar-project.properties` - SonarCloud config
- `.github/SONARQUBE_SETUP.md` - Detailed setup guide

### ✅ Workflow Berjalan Otomatis:
- Saat push ke `main` atau `develop`
- Saat ada Pull Request
- Manual trigger (workflow_dispatch)

### ✅ Badge di README:
README sudah dilengkapi dengan badges:
- Quality Gate Status
- Bugs Count
- Code Smells
- Coverage Percentage

---

## 🔧 Troubleshooting

### ❌ "You are running CI analysis while Automatic Analysis is enabled"
**Fix:** 
1. Login ke https://sonarcloud.io
2. Pilih project **Posind-HCIS_hrms_custom**
3. Klik tab **Administration** (di menu project, bukan organization)
4. Pilih **Analysis Method** (sidebar kiri)
5. **DISABLE "Automatic Analysis"** - toggle ke OFF
6. Pilih **"GitHub Actions"** atau **"CI-based analysis"**
7. Klik **Save**

**Alternatif jika tidak ada Analysis Method:**
1. Di project page, clik **Project Settings**
2. Scroll ke **General Settings**
3. Cari opsi **"Automatic Analysis"**
4. Set ke **OFF** atau **Disabled**

### ❌ "Error: SONAR_TOKEN not found"
**Fix:** Pastikan secret `SONAR_TOKEN` sudah ditambahkan di GitHub repo settings

### ❌ "Project not found"
**Fix:** 
1. Pastikan project key: `Posind-HCIS_hrms_custom`
2. Pastikan organization: `posind-hcis`
3. Cek di SonarCloud apakah project sudah dibuat

### ❌ "Quality Gate failed"
**Fix:** Normal! Lihat detail di SonarCloud dashboard dan fix issues yang ditemukan

### ❌ "No coverage report"
**Fix:** Normal untuk repo baru tanpa tests. Coverage akan muncul setelah ada unit tests.

---

## 📚 Dokumentasi Lengkap

Lihat: `.github/SONARQUBE_SETUP.md` untuk:
- Setup SonarQube self-hosted
- Local analysis
- Advanced configuration
- Badge customization

---

## ✅ Checklist

- [ ] Login SonarCloud dengan GitHub
- [ ] Create project `Posind-HCIS_hrms_custom`
- [ ] Generate token
- [ ] Add `SONAR_TOKEN` ke GitHub secrets
- [ ] Commit & push workflow files
- [ ] Verifikasi workflow berjalan
- [ ] Check hasil di SonarCloud dashboard

---

**Setelah setup selesai, setiap push akan otomatis dianalisis!** 🎉

Dashboard: https://sonarcloud.io/project/overview?id=Posind-HCIS_hrms_custom
