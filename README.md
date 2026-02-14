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

# 🚀 Panduan Deploy Fikri Production ke Server Beneran

## 📋 Persiapan

### Yang Sudah Beres di VM (Tinggal Copy):
- ✅ Flask app (`fikri-production`)
- ✅ Virtual environment (`venv`)
- ✅ Systemd service (`fikri-production.service`)
- ✅ Nginx config
- ✅ Database SQLite (`database.db`)

### Yang Perlu Disiapkan di Server Baru:
- [ ] Server Debian/Ubuntu dengan IP publik
- [ ] Domain (opsional, bisa pakai Ngrok dulu)
- [ ] Akses SSH ke server

---

## 🔄 Transfer Project dari VM ke Server

### Method 1: Pakai Git (Recommended)

**Di VM:**
```bash
cd /home/fikri/apps/fikri-production

# Init git
git init
git add .
git commit -m "Initial commit"

# Push ke GitHub
git remote add origin https://github.com/USERNAME/fikri-production.git
git branch -M main
git push -u origin main
```

**Di Server Baru:**
```bash
git clone https://github.com/USERNAME/fikri-production.git
cd fikri-production
```

### Method 2: Pakai SCP

**Di komputer lokal (bukan di VM):**
```bash
# Compress project
cd /home/fikri/apps
tar -czf fikri-production.tar.gz fikri-production/

# Upload ke server
scp fikri-production.tar.gz user@SERVER-IP:~/

# Di server, extract:
tar -xzf fikri-production.tar.gz
```

---

## ⚙️ Setup di Server Baru (Step-by-Step)

### 1. Update Sistem

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Dependencies

```bash
sudo apt install -y \
    python3 python3-pip python3-venv \
    nginx supervisor git curl wget ufw
```

### 3. Setup Project

```bash
# Buat user
sudo adduser fikri
sudo usermod -aG sudo fikri
su - fikri

# Copy project ke home
cd ~/apps/fikri-production

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Test run
python app.py
# Kalau OK, Ctrl+C untuk stop
```

### 4. Setup Gunicorn Service

```bash
sudo nano /etc/systemd/system/fikri-production.service
```

**Paste config (sesuaikan path!):**

```ini
[Unit]
Description=Fikri Production Flask App
After=network.target

[Service]
User=fikri
Group=fikri
WorkingDirectory=/home/fikri/apps/fikri-production
Environment="PATH=/home/fikri/apps/fikri-production/venv/bin"

ExecStart=/home/fikri/apps/fikri-production/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    --timeout 120 \
    --log-level info \
    app:app

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl enable fikri-production
sudo systemctl start fikri-production
sudo systemctl status fikri-production
```

### 5. Setup Nginx

```bash
sudo nano /etc/nginx/sites-available/fikri-production
```

**Config Nginx:**

```nginx
server {
    listen 80;
    server_name IP-SERVER-KAMU;  # Ganti dengan IP atau domain
    
    client_max_body_size 20M;

    location /static/ {
        alias /home/fikri/apps/fikri-production/static/;
        expires 30d;
        access_log off;
    }

    location /uploads/ {
        alias /home/fikri/apps/fikri-production/uploads/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        proxy_connect_timeout 120;
        proxy_send_timeout 120;
        proxy_read_timeout 120;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/fikri-production /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test & restart
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Setup Firewall

```bash
sudo ufw enable
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw status
```

### 7. Fix Permissions

```bash
sudo chmod 755 /home/fikri
sudo chmod 755 /home/fikri/apps
sudo chmod -R 755 /home/fikri/apps/fikri-production
sudo chown -R fikri:www-data /home/fikri/apps/fikri-production
```

---

## 🌐 Deploy ke Internet (Pilih Salah Satu)

### Option 1: Pakai Ngrok (Termudah)

```bash
# Install ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# Add authtoken (dari ngrok.com)
ngrok config add-authtoken YOUR-TOKEN

# Run dengan screen (agar tetap jalan)
apt install screen -y
screen -S ngrok
ngrok http 8000

# Detach: Ctrl+A lalu D
# Reattach: screen -r ngrok
```

**Atau buat service:**

```bash
sudo nano /etc/systemd/system/ngrok.service
```

```ini
[Unit]
Description=Ngrok Tunnel
After=network.target fikri-production.service

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/ngrok http 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable ngrok
sudo systemctl start ngrok
```

### Option 2: Port Forwarding + DuckDNS (Gratis, Butuh IP Publik)

**Setup DuckDNS:**

```bash
mkdir ~/duckdns
cd ~/duckdns
nano duck.sh
```

```bash
#!/bin/bash
echo url="https://www.duckdns.org/update?domains=SUBDOMAIN&token=TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -
```

```bash
chmod 700 duck.sh
./duck.sh
cat duck.log  # Harus: OK

# Auto update
crontab -e
# Tambahkan:
*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
```

**Setup port forwarding di router:**
- Port 80 → IP-SERVER:80
- Port 443 → IP-SERVER:443

**Install SSL:**

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d subdomain.duckdns.org
```

### Option 3: VPS Cloud (Production)

Deploy ke VPS (DigitalOcean/Vultr/Contabo):
- Ikuti semua step 1-7 di atas
- Tidak perlu port forwarding (VPS punya IP publik langsung)
- Setup domain → point ke IP VPS
- Install SSL dengan certbot

---

## 🔒 Security Checklist

Sebelum production:

```bash
# 1. Ganti secret key di app.py
nano app.py
# Ubah: app.secret_key = os.urandom(24).hex()

# 2. Ganti password admin
# Di app.py, route /admin/login, ubah password

# 3. Install fail2ban
sudo apt install fail2ban -y
sudo systemctl enable fail2ban

# 4. Setup auto backup
nano ~/backup-db.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/fikri/backups"
mkdir -p $BACKUP_DIR
cp /home/fikri/apps/fikri-production/database.db \
   $BACKUP_DIR/database_$DATE.db
find $BACKUP_DIR -name "database_*.db" -mtime +7 -delete
```

```bash
chmod +x ~/backup-db.sh
crontab -e
# Tambahkan:
0 2 * * * /home/fikri/backup-db.sh
```

---

## 📊 Monitoring

```bash
# Check services
sudo systemctl status fikri-production
sudo systemctl status nginx

# View logs
sudo journalctl -u fikri-production -f
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Resource usage
htop
df -h
```

---

## 🐛 Troubleshooting

### Website tidak muncul:
```bash
# Check Gunicorn
sudo systemctl status fikri-production
curl http://localhost:8000

# Check Nginx
sudo systemctl status nginx
sudo nginx -t
```

### CSS tidak load (403 Forbidden):
```bash
sudo chmod 755 /home/fikri
sudo chmod -R 755 /home/fikri/apps/fikri-production
sudo chown -R fikri:www-data /home/fikri/apps/fikri-production
sudo systemctl restart nginx
```

### 502 Bad Gateway:
```bash
# Restart services
sudo systemctl restart fikri-production
sudo systemctl restart nginx

# Check logs
sudo journalctl -u fikri-production -n 50
```

---

## 📁 File yang Perlu Dibawa dari VM

```
/home/fikri/apps/fikri-production/
├── app.py                          # Main application
├── requirements.txt                # Dependencies
├── database.db                     # Database (atau buat baru)
├── static/                         # CSS, JS
├── templates/                      # HTML templates
├── uploads/                        # Upload folder (buat baru)
└── venv/                          # Skip, install ulang di server
```

**File config system:**
```
/etc/systemd/system/fikri-production.service
/etc/nginx/sites-available/fikri-production
```

---

## ⏱️ Estimasi Waktu Setup

- Setup dasar server: **15 menit**
- Transfer & install project: **10 menit**
- Configure Nginx + Service: **10 menit**
- Setup Ngrok/SSL: **10 menit**
- Testing & debug: **15 menit**

**Total: ~1 jam** (kalau smooth)

---

## 🎯 Quick Commands Cheat Sheet

```bash
# Restart app
sudo systemctl restart fikri-production

# Restart Nginx
sudo systemctl restart nginx

# Check logs
sudo journalctl -u fikri-production -f

# Update code
cd ~/apps/fikri-production
git pull
sudo systemctl restart fikri-production

# Backup database
cp database.db database.db.backup

# Test local
curl http://localhost:8000
```

---

## 📞 Kontak Jika Ada Masalah

Kalau besok ada stuck, inget:
1. Check service status dulu
2. Check logs untuk error
3. Google error message
4. Atau tanya lagi! 😊

---

**Good luck untuk deploy besok!** 🚀

Tips: Screenshot semua step yang berhasil di VM, biar besok tinggal ikutin! 📸