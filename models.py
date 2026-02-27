"""
Fikri Production – Database layer using built-in sqlite3
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = None  # set by init_db()


def init_db(app):
    """Initialize database path and create tables"""
    global DB_PATH
    instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    DB_PATH = os.path.join(instance_dir, 'database.db')
    
    conn = get_conn()
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS pesanan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama VARCHAR(100) NOT NULL,
            kontak VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            jenis_print VARCHAR(50) NOT NULL,
            warna VARCHAR(20) NOT NULL,
            ukuran VARCHAR(20) NOT NULL,
            jenis_kertas VARCHAR(50) NOT NULL,
            jumlah INTEGER NOT NULL,
            tanggal_ambil VARCHAR(20) NOT NULL,
            catatan TEXT,
            file_paths TEXT,
            nomor_antrian VARCHAR(20) UNIQUE NOT NULL,
            status VARCHAR(20) DEFAULT "pending",
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS posters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(100) NOT NULL,
            image_path VARCHAR(255) NOT NULL,
            title VARCHAR(200),
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


STATUS_MAP = {'pending': 'Menunggu', 'proses': 'Diproses', 'selesai': 'Selesai'}


def row_to_pesanan(row):
    if not row:
        return None
    d = dict(row)
    files = []
    if d.get('file_paths'):
        try:
            files = json.loads(d['file_paths'])
        except Exception:
            files = []
    d['files'] = files
    d['file_count'] = len(files)
    d['status_indo'] = STATUS_MAP.get(d['status'], d['status'])
    return d


def get_all_pesanan(status_filter='', search=''):
    conn = get_conn()
    c = conn.cursor()
    params = []
    where = []
    if status_filter:
        where.append('status = ?')
        params.append(status_filter)
    if search:
        where.append('(nama LIKE ? OR nomor_antrian LIKE ? OR email LIKE ? OR kontak LIKE ?)')
        params += [f'%{search}%'] * 4
    sql = 'SELECT * FROM pesanan'
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    sql += ' ORDER BY created_at DESC'
    c.execute(sql, params)
    rows = c.fetchall()
    conn.close()
    return [row_to_pesanan(r) for r in rows]


def get_pesanan_by_id(pesanan_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM pesanan WHERE id = ?', (pesanan_id,))
    row = c.fetchone()
    conn.close()
    return row_to_pesanan(row)


def get_pesanan_by_nomor(nomor):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM pesanan WHERE nomor_antrian = ?', (nomor,))
    row = c.fetchone()
    conn.close()
    return row_to_pesanan(row)


def create_pesanan(data):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        INSERT INTO pesanan (nama, kontak, email, jenis_print, warna, ukuran,
          jenis_kertas, jumlah, tanggal_ambil, catatan, file_paths, nomor_antrian, status)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        data['nama'], data['kontak'], data['email'], data['jenis_print'],
        data['warna'], data['ukuran'], data['jenis_kertas'], data['jumlah'],
        data['tanggal_ambil'], data.get('catatan'), data.get('file_paths'),
        data['nomor_antrian'], 'pending'
    ))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return new_id


def update_pesanan_status(pesanan_id, new_status):
    conn = get_conn()
    c = conn.cursor()
    c.execute('UPDATE pesanan SET status = ? WHERE id = ?', (new_status, pesanan_id))
    conn.commit()
    conn.close()


def delete_pesanan_db(pesanan_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('DELETE FROM pesanan WHERE id = ?', (pesanan_id,))
    conn.commit()
    conn.close()


def generate_nomor_antrian():
    today = datetime.now().strftime('%Y%m%d')
    prefix = f"{today}-"
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM pesanan WHERE nomor_antrian LIKE ?", (prefix + '%',))
    count = c.fetchone()[0]
    conn.close()
    return f"{prefix}{str(count + 1).zfill(3)}"


def get_statistics():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM pesanan")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM pesanan WHERE status='pending'")
    pending = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM pesanan WHERE status='proses'")
    proses = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM pesanan WHERE status='selesai'")
    selesai = c.fetchone()[0]
    conn.close()
    return {'total': total, 'pending': pending, 'proses': proses, 'selesai': selesai}


def get_all_posters():
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM posters ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_poster_by_id(poster_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM posters WHERE id = ?', (poster_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def create_poster(data):
    conn = get_conn()
    c = conn.cursor()
    c.execute('INSERT INTO posters (product_name, image_path, title, description) VALUES (?,?,?,?)',
              (data['product_name'], data['image_path'], data.get('title'), data.get('description')))
    conn.commit()
    conn.close()


def delete_poster_db(poster_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('DELETE FROM posters WHERE id = ?', (poster_id,))
    conn.commit()
    conn.close()
