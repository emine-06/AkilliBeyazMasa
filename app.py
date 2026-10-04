import sqlite3
from datetime import datetime
import zoneinfo
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# --- VERİTABANI OLUŞTURMA VE ŞEMA YENİLEME ---
def init_db():
    db_path = 'ankara_beyaz_masa.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Eski/uyumsuz sütun yapısı varsa tabloyu yeniler
    cursor.execute("PRAGMA table_info(talepler)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'aciliyet' in columns or 'tahmin_kategori' in columns or 'kategori' not in columns:
        cursor.execute("DROP TABLE IF EXISTS talepler")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS talepler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT,
            telefon TEXT,
            ilce TEXT,
            mahalle TEXT,
            sikayet_metni TEXT,
            kategori TEXT,
            tarih TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Uygulama başlarken veritabanı yapısını kontrol et
init_db()

# --- YAPAY ZEKA KATEGORİLEŞTİRME MOTORU ---
def yapay_zeka_kategorize_et(metin):
    metin_alt = metin.lower()
    
    if any(kelime in metin_alt for kelime in ['otobüs', 'metro', 'durak', 'sefer', 'ego', 'şoför', 'ulaşım', 'trafik', 'otobus']):
        return 'Ulaşım & EGO'
    elif any(kelime in metin_alt for kelime in ['su', 'patlak', 'boru', 'kanalizasyon', 'lağım', 'aski', 'akıyor', 'kesinti']):
        return 'Su & ASKİ / Altyapı'
    elif any(kelime in metin_alt for kelime in ['çöp', 'koku', 'temizlik', 'sokak', 'park', 'konteynır', 'bozuk', 'kaldırım', 'cop']):
        return 'Çevre & Çöp & Park'
    elif any(kelime in metin_alt for kelime in ['köpek', 'kedi', 'hayvan', 'saldırgan', 'barınak', 'veteriner', 'kopek']):
        return 'Çevre & Sahipsiz Hayvanlar'
    elif any(kelime in metin_alt for kelime in ['yardım', 'gıda', 'koli', 'burs', 'sosyal', 'nakdi', 'destek', 'yardim']):
        return 'Sosyal Hizmetler & Yardım'
    else:
        return 'Genel Şikayet / Diğer'

# --- ROTALAR ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/talep-gonder', methods=['POST'])
def talep_gonder():
    ad_soyad = request.form.get('ad_soyad')
    telefon = request.form.get('telefon')
    ilce = request.form.get('ilce')
    mahalle = request.form.get('mahalle')
    sikayet_metni = request.form.get('sikayet_metni')
    
    # Yapay zeka ile kategori tespiti
    kategori = yapay_zeka_kategorize_et(sikayet_metni)
    
    # Türkiye saatine (UTC+3) göre anlık saat ve tarih alımı
    turkiye_saati = zoneinfo.ZoneInfo("Europe/Istanbul")
    tarih = datetime.now(turkiye_saati).strftime('%d.%m.%Y %H:%M')
    
    conn = sqlite3.connect('ankara_beyaz_masa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO talepler (ad_soyad, telefon, ilce, mahalle, sikayet_metni, kategori, tarih)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (ad_soyad, telefon, ilce, mahalle, sikayet_metni, kategori, tarih))
    conn.commit()
    conn.close()
    
    return render_template('index.html', mesaj="Başvurunuz başarıyla kaydedilmiştir. Teşekkür ederiz!")

@app.route('/admin')
def admin_panel():
    conn = sqlite3.connect('ankara_beyaz_masa.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, ad_soyad, telefon, ilce, mahalle, sikayet_metni, kategori, tarih FROM talepler ORDER BY id DESC")
    talepler = cursor.fetchall()
    
    cursor.execute("SELECT ilce, COUNT(*) FROM talepler GROUP BY ilce")
    ilce_data = cursor.fetchall()
    ilce_labels = [row[0] for row in ilce_data]
    ilce_values = [row[1] for row in ilce_data]
    
    cursor.execute("SELECT kategori, COUNT(*) FROM talepler GROUP BY kategori")
    kat_data = cursor.fetchall()
    kat_labels = [row[0] for row in kat_data]
    kat_values = [row[1] for row in kat_data]
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                           talepler=talepler, 
                           ilce_labels=ilce_labels, 
                           ilce_values=ilce_values,
                           kat_labels=kat_labels,
                           kat_values=kat_values)

@app.route('/admin/sifirla', methods=['POST'])
def admin_sifirla():
    conn = sqlite3.connect('ankara_beyaz_masa.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM talepler")
    conn.commit()
    conn.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
