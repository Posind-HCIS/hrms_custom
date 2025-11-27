# Instalasi Frappe, HRMS, dan HRMS Custom

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Posind-HCIS_hrms_custom&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Posind-HCIS_hrms_custom)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Posind-HCIS_hrms_custom&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Posind-HCIS_hrms_custom)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Posind-HCIS_hrms_custom&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Posind-HCIS_hrms_custom)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Posind-HCIS_hrms_custom&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Posind-HCIS_hrms_custom)

Modul kustom untuk memperluas HRMS di Frappe/ERPNext. Menambahkan fitur seperti doctype kustom, laporan, dan alur kerja.

## Persyaratan (Requirements)

- Python 3.10+
- Node.js 18+
- MariaDB 10.3+ atau PostgreSQL 12+
- Redis 5+
- OS: Ubuntu 22.04 LTS direkomendasikan

## Instalasi dari Awal (Installation from Scratch)

Ikuti langkah-langkah ini untuk menyiapkan bench Frappe baru, membuat situs, menginstal HRMS resmi, dan menambahkan aplikasi kustom ini dari GitHub.

### 1. Inisialisasi Bench (Init Bench - Setup Lingkungan Frappe)

```bash
# Instal bench
pip3 install frappe-bench

# Inisialisasi bench (ganti `mybench` dengan nama bench Anda)
bench init mybench
cd mybench

# Dapatkan Frappe dari branch stabil
bench get-app --branch version-15 frappe
```

### 2. Buat Situs (Create Site)

```bash
# Buat situs baru (ganti `mysite.local` dengan nama situs Anda)
bench new-site mysite.local

# Atur kata sandi admin (opsional)
bench --site mysite.local set-admin-password 'admin123'
```

Akses di browser: `http://mysite.local` (login: Administrator / admin123).

### 3. Instal ERPNext (Diperlukan untuk HRMS)

```bash
# Dapatkan ERPNext dari branch stabil
bench get-app --branch version-15 erpnext

# Instal ke situs
bench --site mysite.local install-app erpnext

# Migrasi DB
bench --site mysite.local migrate
```

### 4. Instal HRMS Resmi (Install Official HRMS)

```bash
# Dapatkan HRMS dari repo GitHub resmi (branch stabil)
bench get-app --branch version-15 hrms https://github.com/frappe/hrms.git

# Instal ke situs
bench --site mysite.local install-app hrms

# Migrasi DB
bench --site mysite.local migrate
bench restart
```

### 5. Instal HRMS Custom dari GitHub (Install HRMS Custom from GitHub)

```bash
# Dapatkan app kustom dari repo Anda
bench get-app hrms_custom https://github.com/Posind-HCIS/hrms_custom.git --branch main

# Instal ke situs
bench --site mysite.local install-app hrms_custom

# Migrasi DB untuk perubahan kustom
bench --site mysite.local migrate

# Bangun aset & restart
bench build
bench restart
```

Modul kustom siap! Refresh browser; seharusnya muncul di Desk (jika tidak, jalankan `bench --site mysite.local clear-cache`).

## Pembaruan App dari GitHub (Update App from GitHub)

Untuk pembaruan:

```bash
cd apps/hrms_custom
git pull origin main
cd ../..

bench update --apps hrms_custom
bench --site mysite.local migrate
bench restart
```

## Pemecahan Masalah (Troubleshooting)

- **Error 503**: Tunggu 1-2 menit selama migrasi/build.
- **Modul Tidak Terlihat**: `bench --site mysite.local clear-cache && bench restart`. Untuk v15+, buat Workspace baru dan tetapkan modul.
- **Kesalahan Impor**: Pastikan `hrms_custom/hrms_custom/__init__.py` ada; restart bench.
- **Mode Pengembang**: Untuk pembuatan kode: `bench set-config -g developer_mode 1 && bench restart`.

