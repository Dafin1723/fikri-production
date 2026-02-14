# 🖨️ Fikri Production - Unit Produksi Web App

Web application untuk Unit Produksi dan Fotokopi SMKIT Ihsanul Fikri Mungkid. Sistem pemesanan print online dengan manajemen admin.

## 📋 Fitur Utama

### 👥 User Features
- ✅ Katalog produk/jasa (Document Print, Custom T-Shirt, Mug, Sticker, dll)
- ✅ Form pemesanan dengan upload file
- ✅ Preview file sebelum submit (Image, PDF, Document)
- ✅ Cek status pesanan dengan nomor order
- ✅ Timeline progress pesanan (Pending → Proses → Selesai)

### 🔐 Admin Features
- ✅ Login admin dengan session
- ✅ Dashboard statistik real-time (Total, Pending, Process, Complete)
- ✅ Filter pesanan by status (All, Pending, Process, Complete)
- ✅ Search pesanan by nama atau kontak
- ✅ Update status pesanan
- ✅ Download file pesanan
- ✅ Export data ke Excel (.xlsx)
- ✅ Export data ke PDF (.pdf)

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Export**: Pandas (Excel), ReportLab (PDF)

## 📁 Struktur Project

```
fikri_production/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── database.db                 # SQLite database (auto-generated)
├── uploads/                    # Folder untuk file upload (auto-generated)
├── static/
│   ├── css/
│   │   ├── style.css          # CSS utama untuk user pages
│   │   └── admin.css          # CSS untuk admin dashboard
│   ├── js/
│   └── images/
└── templates/
    ├── produk.html             # Landing page & katalog
    ├── user/
    │   ├── index.html          # Form pemesanan
    │   └── cek_status.html     # Cek status pesanan
    └── admin/
        ├── login.html          # Login admin
        └── dashboard.html      # Dashboard admin
```

## 🚀 Cara Instalasi & Menjalankan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi

```bash
python app.py
```

### 3. Akses di Browser

- **User Interface**: http://127.0.0.1:5000/
- **Admin Login**: http://127.0.0.1:5000/admin/login

### 4. Login Admin

```
Username: admin
Password: unitproduksi123
```

## 📊 Database Schema

### Model: Pesanan

| Field        | Type      | Description                    |
|--------------|-----------|--------------------------------|
| id           | Integer   | Primary key (auto-increment)   |
| nama         | String    | Nama pemesan                   |
| kontak       | String    | Email/WhatsApp                 |
| jenis_print  | String    | Jenis print/produk             |
| ukuran       | String    | Ukuran kertas/produk           |
| jumlah       | Integer   | Jumlah copies                  |
| file_path    | String    | Path file upload               |
| status       | String    | pending/proses/selesai         |
| created_at   | DateTime  | Timestamp pemesanan            |

## 🎨 Design System

### Color Palette
- **Primary Orange**: `#FF8C42`
- **Secondary Peach**: `#FFE5D9`
- **Dark Blue**: `#0047FF`
- **Success Green**: `#28a745`
- **Warning Yellow**: `#ffc107`
- **Danger Red**: `#dc3545`

### Typography
- **Font Family**: Inter, Segoe UI, Tahoma, Geneva, Verdana, sans-serif

## 📝 User Flow

### Alur Pemesanan (User)
1. User membuka landing page → melihat katalog
2. Klik "Order Now" → Form pemesanan
3. Isi data (Nama, Kontak, Jenis Print, Ukuran, Jumlah)
4. Upload file desain → Preview otomatis
5. Submit → Mendapat nomor pesanan
6. Cek status dengan nomor pesanan

### Alur Management (Admin)
1. Login di `/admin/login`
2. Dashboard menampilkan statistik real-time
3. Filter pesanan by status atau search
4. Update status pesanan (Pending → Proses → Selesai)
5. Download file pesanan
6. Export data ke Excel/PDF

## 🔒 Security Notes

⚠️ **PENTING**: Sebelum deploy ke production:

1. **Ganti Secret Key**:
   ```python
   app.secret_key = os.urandom(24)  # Generate random key
   ```

2. **Ganti Password Admin**:
   - Implementasi hash password (bcrypt)
   - Jangan hardcode credentials

3. **Validasi File Upload**:
   - Sudah ada validasi extension
   - Tambahkan validasi size & content type

4. **HTTPS**: Deploy dengan HTTPS di production

## 🌐 API Endpoints

### Public Routes
- `GET /` - Redirect ke produk
- `GET /produk` - Landing page & katalog
- `GET/POST /pesan` - Form pemesanan
- `GET/POST /cek-status` - Cek status pesanan

### Admin Routes (Protected)
- `GET/POST /admin/login` - Login admin
- `GET /admin/logout` - Logout admin
- `GET /admin` - Dashboard (dengan filter & search)
- `POST /update/<id>` - Update status pesanan
- `GET /download/<filename>` - Download file
- `GET /admin/export/excel` - Export ke Excel
- `GET /admin/export/pdf` - Export ke PDF
- `GET /admin/api/stats` - API statistik (JSON)

## 👥 Tim Pengembang

**THE FOOL Team** - Pembagian Tugas:
- **Dafin**: Struktur awal, config, routing, file upload/download, session
- **Amru**: Database model, inisialisasi database, template produk
- **Fikri**: Admin routes, login/logout, dashboard, update status, flash messages

## 📱 Responsive Design

- ✅ Desktop (1920px+)
- ✅ Tablet (768px - 1024px)
- ✅ Mobile (< 768px)

## 🐛 Troubleshooting

### Database tidak terbuat?
```bash
# Di Python shell:
from app import app, db
with app.app_context():
    db.create_all()
```

### Error import pandas/reportlab?
```bash
pip install pandas openpyxl reportlab --break-system-packages
```

### File upload tidak berfungsi?
- Cek folder `uploads/` sudah ada
- Cek permission folder (chmod 755)

## 📄 License

© 2025 Fikri Production - SMKIT Ihsanul Fikri Mungkid

---

**Catatan**: Ini adalah project tugas sekolah untuk Unit Produksi. Untuk penggunaan production, pastikan implementasi security yang lebih robust.
