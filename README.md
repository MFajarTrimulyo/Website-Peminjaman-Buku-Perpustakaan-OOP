# 📚 Website Peminjaman Buku Perpustakaan

Aplikasi sistem peminjaman buku perpustakaan berbasis web yang dibangun dengan **Flask (Python)** dan menerapkan konsep **Object-Oriented Programming (OOP)**. Aplikasi ini ditujukan untuk **pustakawan** dalam mengelola data **anggota perpustakaan**, **buku**, serta **transaksi peminjaman dan pengembalian**.

## 📖 Deskripsi Aplikasi

Aplikasi ini memudahkan pengelolaan perpustakaan secara digital dengan menyediakan antarmuka sederhana namun lengkap untuk pustakawan. Setiap entitas utama dalam sistem (anggota, buku, peminjaman) dimodelkan sebagai kelas dalam OOP dan dihubungkan dengan database MySQL.

---

## 🚀 Fitur-Fitur

* ✅ CRUD Data Anggota (Mahasiswa & Dosen)
* ✅ CRUD Data Buku
* ✅ CRUD Jenis Buku, Penerbit, Penulis, dan Sumber Buku
* ✅ Transaksi Peminjaman dan Pengembalian Buku
* ✅ Validasi NIM/NIP Anggota (berdasarkan panjang karakter)
* ✅ Desain modular dengan OOP
* ✅ Routing berbasis Blueprint di Flask

---

## 🧱 Struktur Proyek

```
Website-Peminjaman-Buku-Perpustakaan-OOP/
│
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── anggota.py
│   │   ├── buku.py
│   │   ├── peminjaman.py
│   │   └── ...
│   ├── models/
│   │   ├── anggota.py
│   │   ├── buku.py
│   │   ├── jenis_buku.py
│   │   └── ...
│   └── templates/
│       └── *.html
│
├── static/
│   └── css/, js/, dll
│
├── config.py
├── requirements.txt
└── run.py
```

---

## 🧠 Struktur OOP

### 🔹 Kelas Utama

* `Anggota` (superclass)

  * `Mahasiswa` (subclass)
  * `Dosen` (subclass)
* `Buku`
* `Penerbit`
* `Penulis`
* `JenisBuku`
* `SumberBuku`
* `Peminjaman`

### 🔹 Konsep OOP yang Diterapkan

* **Encapsulation** – Setiap entitas diwakili oleh kelas dan data disimpan sebagai atribut.
* **Inheritance** – `Mahasiswa` dan `Dosen` mewarisi dari kelas `Anggota`.
* **Polymorphism** – Method berbeda dengan nama yang sama pada subclass.
* **Abstraction** – Penggunaan class untuk menyembunyikan detail implementasi dan hanya menyediakan antarmuka publik.

---

## ⚙️ Instalasi & Menjalankan Aplikasi

1. **Clone repository:**

```bash
git clone https://github.com/MFajarTrimulyo/Website-Peminjaman-Buku-Perpustakaan-OOP.git
cd Website-Peminjaman-Buku-Perpustakaan-OOP
```

2. **Buat virtual environment dan aktifkan:**

```bash
python -m venv venv
source venv/bin/activate  # untuk Linux/Mac
venv\Scripts\activate     # untuk Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Konfigurasikan database (MySQL):**

   * Pastikan MySQL aktif.
   * Buat database dan sesuaikan konfigurasi di `config.py`.

5. **Jalankan aplikasi:**

```bash
python run.py
```

---

## 📸 Screenshot Tampilan Aplikasi

> (Tambahkan tangkapan layar antarmuka aplikasi di sini)

---
