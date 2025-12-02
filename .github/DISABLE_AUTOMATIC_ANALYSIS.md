# 🔧 Cara Disable Automatic Analysis di SonarCloud

## ⚠️ Error yang Muncul:
```
ERROR: You are running CI analysis while Automatic Analysis is enabled. 
Please consider disabling one or the other.
```

---

## 📍 **Lokasi yang Benar**

**❌ SALAH:** Organization Settings (yang ada di screenshot Anda)  
**✅ BENAR:** Project Settings

---

## 🎯 **Langkah-langkah yang Benar**

### **Step 1: Buka Project (Bukan Organization)**

1. Di SonarCloud, klik logo **SonarCloud** di pojok kiri atas untuk kembali ke dashboard
2. Atau langsung buka: https://sonarcloud.io/projects
3. **Pilih project:** `Posind-HCIS_hrms_custom`

### **Step 2: Masuk ke Project Administration**

1. Setelah masuk ke project page
2. Klik tab **"Administration"** (di menu project, bukan organization!)
3. Di sidebar kiri, cari menu **"Analysis Method"**

### **Step 3: Disable Automatic Analysis**

Anda akan lihat 2 opsi:

#### **Option A: Automatic Analysis** ❌
- Deskripsi: "SonarCloud automatically analyzes your code"
- **ACTION: Toggle ini ke OFF / Disable**

#### **Option B: CI-Based Analysis** ✅  
- Deskripsi: "Analysis via GitHub Actions, Azure Pipelines, etc."
- **ACTION: Pilih opsi ini**

### **Step 4: Save**

Klik tombol **"Save"** di bagian bawah

---

## 🔍 **Jika Tidak Ada Menu "Analysis Method"**

Beberapa kemungkinan:

### **Kemungkinan 1: Project Belum Dibuat**
Pastikan project sudah dibuat:
1. Buka: https://sonarcloud.io/projects
2. Cek apakah `Posind-HCIS_hrms_custom` ada di list
3. Jika belum ada, create project dulu

### **Kemungkinan 2: Analysis Method di General Settings**
1. Di Project Administration, klik **"General Settings"**
2. Scroll ke bagian **"Analysis"**
3. Cari toggle **"Automatic Analysis"**
4. Set ke **OFF/Disabled**

### **Kemungkinan 3: Belum Ada Permission**
1. Pastikan Anda adalah **Admin** atau **Owner** dari project
2. Cek di: Project Settings → Members
3. Role Anda harus **Admin**

---

## 🚀 **Quick Fix via URL**

Langsung buka URL ini (ganti `posind-hcis` dengan organization key yang benar jika berbeda):

```
https://sonarcloud.io/project/admin/extension/developer-server/Posind-HCIS_hrms_custom
```

Atau:

```
https://sonarcloud.io/project/configuration?id=Posind-HCIS_hrms_custom&analysisMode=manual
```

---

## 📸 **Visual Guide**

### **Navigasi yang Benar:**

```
SonarCloud Dashboard
  └─ Projects (sidebar)
      └─ Posind-HCIS_hrms_custom (pilih project)
          └─ Administration (tab atas)
              └─ Analysis Method (sidebar kiri)
                  └─ [Toggle OFF] Automatic Analysis
                  └─ [Select] CI-Based Analysis
                  └─ [Click] Save
```

### **BUKAN ini (yang Anda buka):**

```
SonarCloud Dashboard
  └─ Administration (dropdown kanan atas)  ❌ INI ORGANIZATION SETTINGS
      └─ Posind-HCIS (organization)
          └─ Organization Settings
```

---

## ✅ **Cara Verifikasi Sudah Benar**

Setelah disable, coba:

1. **Re-run GitHub Actions:**
   ```bash
   # Trigger workflow lagi dengan push kosong
   git commit --allow-empty -m "chore: trigger workflow after disabling automatic analysis"
   git push origin main
   ```

2. **Check di GitHub Actions:**
   - Buka: https://github.com/Posind-HCIS/hrms_custom/actions
   - Workflow seharusnya **SUCCESS** ✅
   - Tidak ada error "Automatic Analysis enabled"

3. **Check di SonarCloud:**
   - Dashboard project akan menunjukkan "Last analysis"
   - Analysis method: **GitHub Actions** atau **CI**

---

## 💡 **Tips**

1. **Matikan dulu Automatic Analysis** sebelum setup GitHub Actions
2. **Pilih satu method saja:** Automatic ATAU CI-based (tidak bisa dua-duanya)
3. **GitHub Actions lebih control:** Anda bisa customize kapan analysis berjalan

---

## 📞 **Masih Error?**

Jika masih error, bisa jadi:

1. **Cache issue:** Wait 5-10 menit, SonarCloud perlu sinkronisasi
2. **Token issue:** Regenerate SONAR_TOKEN dan update di GitHub secrets
3. **Project key salah:** Double-check `sonar.projectKey=Posind-HCIS_hrms_custom`

---

**Good luck!** 🚀

Setelah disable Automatic Analysis, workflow akan berjalan normal tanpa conflict.
