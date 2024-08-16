import sqlite3

def createTable():

    # Veritabanı dosyasını oluştur veya bağlan
    conn = sqlite3.connect('Database.sql')
    c = conn.cursor()

    # Dersler tablosunu oluştur
    c.execute('''
        CREATE TABLE IF NOT EXISTS Dersler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL
        )
    ''')

    # Konular tablosunu oluştur
    c.execute('''
        CREATE TABLE IF NOT EXISTS Konular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ders_id INTEGER,
            ad TEXT NOT NULL,
            FOREIGN KEY (ders_id) REFERENCES Dersler(id)
        )
    ''')

    # Testler tablosunu oluştur
    c.execute('''
        CREATE TABLE IF NOT EXISTS Testler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            konu_id INTEGER,
            ad TEXT NOT NULL,
            FOREIGN KEY (konu_id) REFERENCES Konular(id)
        )
    ''')

    # Sorular tablosunu oluştur
    c.execute('''
        CREATE TABLE IF NOT EXISTS Sorular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER,
            soru TEXT NOT NULL,
            dogru_sik TEXT NOT NULL,
            FOREIGN KEY (test_id) REFERENCES Testler(id)
        )
    ''')

    # Şıklar tablosunu oluştur
    c.execute('''
        CREATE TABLE IF NOT EXISTS Sıklar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soru_id INTEGER,
            sik TEXT NOT NULL,
            FOREIGN KEY (soru_id) REFERENCES Sorular(id)
        )
    ''')

    # Değişiklikleri kaydet ve bağlantıyı kapat
    conn.commit()
    conn.close()

soru_numarasi = 0
def veri_ekle():
    conn = sqlite3.connect('Database.sql')
    c = conn.cursor()

    ders_ad = input("Ders adı: ")
    c.execute("INSERT INTO Dersler (ad) VALUES (?)", (ders_ad,))
    ders_id = c.lastrowid

    while True:
        konu_ad = input("Konu adı (veya 'bitir' yazın): ")
        if konu_ad.lower() == 'bitir':
            break
        c.execute("INSERT INTO Konular (ders_id, ad) VALUES (?, ?)", (ders_id, konu_ad))
        konu_id = c.lastrowid

        test_ad = input("Test adı: ")
        c.execute("INSERT INTO Testler (konu_id, ad) VALUES (?, ?)", (konu_id, test_ad))
        test_id = c.lastrowid

        while True:
            soru = input(f"[{soru_numarasi}] | Soru (veya 'bitir' yazın): ")
            if soru.lower() == 'bitir':
                break
            soru_numarasi += 1
            dogru_sik = input("Doğru şık: ")
            c.execute("INSERT INTO Sorular (test_id, soru, dogru_sik) VALUES (?, ?, ?)", (test_id, soru, dogru_sik))
            soru_id = c.lastrowid

            for i in range(4):
                sik = input(f"{i+1}. şık: ")
                c.execute("INSERT INTO Sıklar (soru_id, sik) VALUES (?, ?)", (soru_id, sik))

    conn.commit()
    conn.close()
    print("Veriler başarıyla eklendi!")

veri_ekle()