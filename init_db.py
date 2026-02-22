import sqlite3

conn = sqlite3.connect("reports.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    location TEXT NOT NULL,
    observation TEXT NOT NULL,
    severity TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database and table created successfully!")