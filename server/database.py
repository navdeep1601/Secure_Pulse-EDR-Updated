import sqlite3

def init_db():
    conn = sqlite3.connect('mirage_events.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            attacker_ip TEXT,
            port INTEGER,
            service TEXT,
            payload TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_to_db(ip, port, service, payload):
    conn = sqlite3.connect('mirage_events.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO events (attacker_ip, port, service, payload) VALUES (?, ?, ?, ?)', 
                   (ip, port, service, payload))
    conn.commit()
    conn.close()