# SonarQube/SonarCloud Setup Guide

## 🎯 Overview

Repository ini sudah dikonfigurasi untuk menggunakan **SonarCloud** atau **SonarQube** untuk analisis kualitas kode secara otomatis.

---

## 🔧 Setup SonarCloud (Recommended - Free untuk public repos)

### **Step 1: Daftar SonarCloud**

1. Buka https://sonarcloud.io
2. Login dengan GitHub account
3. Klik **"+"** → **"Analyze new project"**
4. Pilih **Posind-HCIS/hrms_custom**
5. Klik **"Set Up"**

### **Step 2: Get Token**

1. Di SonarCloud, klik **Account** → **Security**
2. Di bagian **Generate Tokens**, buat token baru:
   - Name: `GitHub Actions`
   - Type: `Global Analysis Token` atau `Project Analysis Token`
   - Expiration: `No expiration` atau sesuai kebutuhan
3. **Copy token** yang dihasilkan

### **Step 3: Add Token ke GitHub**

1. Buka: https://github.com/Posind-HCIS/hrms_custom/settings/secrets/actions
2. Klik **"New repository secret"**
3. Tambahkan secret:
   - **Name:** `SONAR_TOKEN`
   - **Value:** `<paste token dari step 2>`
4. Klik **"Add secret"**

### **Step 4: Configure Organization**

1. Di SonarCloud, klik **"+"** → **"Create new organization"**
2. Pilih **Import from GitHub**
3. Pilih **Posind-HCIS**
4. Organization key akan otomatis: `posind-hcis`

### **Step 5: Update Configuration (Jika Diperlukan)**

File `.github/workflows/sonarcloud.yml` sudah dikonfigurasi dengan:
```yaml
-Dsonar.projectKey=Posind-HCIS_hrms_custom
-Dsonar.organization=posind-hcis
```

Jika organization key Anda berbeda, update di:
- `.github/workflows/sonarcloud.yml`
- `sonar-project.properties`

---

## 🏢 Setup SonarQube (Self-hosted)

### **Step 1: Install SonarQube Server**

**Via Docker:**
```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:latest
```

**Via Docker Compose:**
```yaml
version: "3"
services:
  sonarqube:
    image: sonarqube:community
    ports:
      - "9000:9000"
    environment:
      - SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_extensions:/opt/sonarqube/extensions
      - sonarqube_logs:/opt/sonarqube/logs

volumes:
  sonarqube_data:
  sonarqube_extensions:
  sonarqube_logs:
```

### **Step 2: Access SonarQube**

1. Buka: `http://localhost:9000`
2. Default login: `admin` / `admin`
3. Ganti password saat diminta

### **Step 3: Create Project**

1. Klik **"Create Project"** → **"Manually"**
2. Project key: `Posind-HCIS_hrms_custom`
3. Display name: `HRMS Custom`
4. Klik **"Set Up"**

### **Step 4: Generate Token**

1. Klik **"Locally"**
2. Generate token:
   - Name: `GitHub Actions`
   - Type: `Project Analysis Token`
3. **Copy token**

### **Step 5: Add Secrets ke GitHub**

Tambahkan 2 secrets:

**Secret 1:**
- Name: `SONAR_TOKEN`
- Value: `<token dari step 4>`

**Secret 2:**
- Name: `SONAR_HOST_URL`
- Value: `http://your-sonarqube-server:9000`

### **Step 6: Enable SonarQube Workflow**

Uncomment dan gunakan workflow di `.github/workflows/ci.yml` bagian `sonarqube` job.

---

## 📊 What Will Be Analyzed?

SonarQube/SonarCloud akan menganalisis:

### **Code Quality Metrics:**
- 🐛 **Bugs** - Kode yang berpotensi error
- 🔒 **Vulnerabilities** - Security issues
- 💩 **Code Smells** - Maintainability issues
- 📊 **Coverage** - Test coverage percentage
- 🔄 **Duplications** - Duplicate code
- 📏 **Technical Debt** - Estimated time to fix issues

### **Language Support:**
- ✅ Python
- ✅ JavaScript
- ✅ HTML/CSS
- ✅ JSON/YAML

---

## 🔍 View Results

### **SonarCloud:**
https://sonarcloud.io/project/overview?id=Posind-HCIS_hrms_custom

### **SonarQube:**
http://your-sonarqube-server:9000/dashboard?id=Posind-HCIS_hrms_custom

### **GitHub:**
- Checks akan muncul di PR
- Status badge bisa ditambahkan ke README

---

## 🎨 Add Badge to README

### **SonarCloud Badge:**
```markdown
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Posind-HCIS_hrms_custom&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Posind-HCIS_hrms_custom)

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Posind-HCIS_hrms_custom&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Posind-HCIS_hrms_custom)

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Posind-HCIS_hrms_custom&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Posind-HCIS_hrms_custom)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Posind-HCIS_hrms_custom&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Posind-HCIS_hrms_custom)

[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=Posind-HCIS_hrms_custom&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=Posind-HCIS_hrms_custom)
```

### **SonarQube Badge:**
```markdown
[![Quality Gate Status](http://your-sonarqube:9000/api/project_badges/measure?project=Posind-HCIS_hrms_custom&metric=alert_status)](http://your-sonarqube:9000/dashboard?id=Posind-HCIS_hrms_custom)
```

---

## 🧪 Local Analysis (Optional)

### **Install SonarScanner:**
```bash
# macOS
brew install sonar-scanner

# Linux
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip sonar-scanner-cli-5.0.1.3006-linux.zip
export PATH=$PATH:$PWD/sonar-scanner-5.0.1.3006-linux/bin
```

### **Run Local Scan:**
```bash
cd /home/rafieaydin/frappe_framework/bench/apps/hrms_custom

# Generate coverage report
pytest --cov=hrms_custom --cov-report=xml

# Run scanner
sonar-scanner \
  -Dsonar.projectKey=Posind-HCIS_hrms_custom \
  -Dsonar.organization=posind-hcis \
  -Dsonar.sources=. \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=YOUR_TOKEN
```

---

## 🔧 Troubleshooting

### **Issue: "No coverage report found"**
**Solution:**
```bash
# Pastikan pytest-cov terinstall
pip install pytest-cov

# Run tests dengan coverage
pytest --cov=hrms_custom --cov-report=xml
```

### **Issue: "Token invalid"**
**Solution:**
1. Generate token baru di SonarCloud/SonarQube
2. Update secret di GitHub

### **Issue: "Project not found"**
**Solution:**
1. Cek `sonar.projectKey` di config
2. Pastikan project sudah dibuat di SonarCloud/SonarQube

### **Issue: "Quality Gate failed"**
**Solution:**
1. Lihat detail di SonarCloud dashboard
2. Fix issues yang ditemukan
3. Push ulang

---

## 📚 Resources

- **SonarCloud Docs:** https://docs.sonarcloud.io/
- **SonarQube Docs:** https://docs.sonarqube.org/
- **Python Analysis:** https://docs.sonarqube.org/latest/analysis/languages/python/
- **GitHub Action:** https://github.com/SonarSource/sonarcloud-github-action

---

## ✅ Checklist

- [ ] Daftar SonarCloud atau install SonarQube
- [ ] Create project dengan key: `Posind-HCIS_hrms_custom`
- [ ] Generate token
- [ ] Add `SONAR_TOKEN` ke GitHub secrets
- [ ] Add `SONAR_HOST_URL` ke secrets (jika SonarQube)
- [ ] Update organization di config (jika berbeda)
- [ ] Push code untuk trigger workflow
- [ ] Verifikasi hasil di dashboard
- [ ] Add badge ke README (optional)

---

**Setelah setup, setiap PR akan otomatis dianalisis!** 🚀
