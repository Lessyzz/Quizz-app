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
            sure_sn INTEGER NOT NULL,
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