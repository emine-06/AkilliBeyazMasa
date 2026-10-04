import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

# Türkçe Şikayet Eğitim Verisi
data = {
    'metin': [
        'Kızılay meydanında çöp konteynerleri dolmuş koku yapıyor',
        'Sokaktaki çöpler toplanmıyor pislik içinde kaldı ortalık',
        'Çöp kovası kırılmış ve etrafa atıklar saçılmış',
        'Yolda dev gibi bir asfalt çukuru var araçların lastiği patlıyor',
        'Kaldırım taşları sökülmüş yürürken düşüp ayağımı burktum',
        'Sokak lambaları yanmıyor cadde çok karanlık ve tehlikeli',
        'Parktaki salıncak ve kaydırak kırık çocuklar oynayamıyor',
        'Yeşil alanların çimleri uzadı ve ağaç dalları yolu kapatıyor',
        'Parktaki oturma bankları kırılmış bakım yapılması lazım',
        'Kaldırımları esnaf tezgahlarla işgal etmiş yürüyecek yer yok',
        'Marketlerde tarihi geçmiş ürün satılıyor denetim yapın',
        'Seyyar satıcılar kaldırımı kapatmış zabıta müdahale etsin',
        'Otobüs durakta durmadı geçti ve saatinde gelmiyor',
        'Eryaman otobüs sefer saatleri yetersiz otobüsler çok kalabalık',
        'Metro yürüyen merdivenleri çalışmıyor yaşlılar zorlanıyor'
    ],
    'kategori': [
        'Temizlik İşleri', 'Temizlik İşleri', 'Temizlik İşleri',
        'Fen İşleri', 'Fen İşleri', 'Fen İşleri',
        'Park ve Bahçeler', 'Park ve Bahçeler', 'Park ve Bahçeler',
        'Zabıta', 'Zabıta', 'Zabıta',
        'Ulaşım Dairesi', 'Ulaşım Dairesi', 'Ulaşım Dairesi'
    ]
}

df = pd.DataFrame(data)

# Modeli Oluştur ve Eğit
model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), MultinomialNB())
model.fit(df['metin'], df['kategori'])

# Modeli Kaydet
joblib.dump(model, 'sikayet_modeli.pkl')
print("✅ NLP Modeli eğitildi ve 'sikayet_modeli.pkl' olarak kaydedildi.")