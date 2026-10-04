import sqlite3

VT_ADI = 'ankara_beyaz_masa.db'

def vt_baglan():
    conn = sqlite3.connect(VT_ADI)
    conn.row_factory = sqlite3.Row
    return conn

def vt_kur():
    conn = vt_baglan()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS talepler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            telefon TEXT,
            ilce TEXT NOT NULL,
            mahalle TEXT,
            sikayet_metni TEXT NOT NULL,
            tahmin_kategori TEXT NOT NULL,
            durum TEXT DEFAULT 'Beklemede',
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def ornek_veri_ekle():
    # Sistem sıfır veriyle başlasın, biz form doldurdukça grafikler aksın diye içi boş bırakıldı!
    pass

def talep_ekle(ad_soyad, telefon, ilce, mahalle, sikayet_metni, tahmin_kategori):
    conn = vt_baglan()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO talepler (ad_soyad, telefon, ilce, mahalle, sikayet_metni, tahmin_kategori)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (ad_soyad, telefon, ilce, mahalle, sikayet_metni, tahmin_kategori))
    conn.commit()
    conn.close()

def tum_talepleri_getir():
    conn = vt_baglan()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM talepler ORDER BY id DESC')
    veriler = cursor.fetchall()
    conn.close()
    return [dict(row) for row in veriler]

def durum_guncelle(talep_id, yeni_durum):
    conn = vt_baglan()
    cursor = conn.cursor()
    cursor.execute('UPDATE talepler SET durum = ? WHERE id = ?', (yeni_durum, talep_id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    vt_kur()
    print("✅ Sıfır Verili Ankara Veritabanı Hazır!")