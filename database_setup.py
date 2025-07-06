import sqlite3

conn = sqlite3.connect("pet_health.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_type TEXT NOT NULL,
    age INTEGER,
    symptoms TEXT,
    conditions TEXT,
    severity_score INTEGER,
    emergency_flag INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
