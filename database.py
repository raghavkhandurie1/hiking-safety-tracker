import sqlite3

def init_db():
    conn = sqlite3.connect("hikes.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hikes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            location TEXT,
            duration_minutes INTEGER,
            distance_km REAL,
            weather_description TEXT,
            temperature REAL,
            notes TEXT,
            emergency_contact TEXT,
            expected_return TEXT,
            checked_in INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()

def save_hike(date, location, duration, distance, weather, temp, notes, emergency_contact, expected_return):
    conn = sqlite3.connect("hikes.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO hikes 
        (date, location, duration_minutes, distance_km, weather_description, temperature, notes, emergency_contact, expected_return, checked_in)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    """, (date, location, duration, distance, weather, temp, notes, emergency_contact, expected_return))
    conn.commit()
    conn.close()

def check_in(hike_id):
    conn = sqlite3.connect("hikes.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE hikes SET checked_in = 1 WHERE id = ?", (hike_id,))
    conn.commit()
    conn.close()

def get_all_hikes():
    conn = sqlite3.connect("hikes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hikes")
    hikes = cursor.fetchall()
    conn.close()
    return hikes

def get_overdue_hikes():
    conn = sqlite3.connect("hikes.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM hikes 
        WHERE checked_in = 0 
        AND expected_return < datetime('now', 'localtime')
    """)
    overdue = cursor.fetchall()
    conn.close()
    return overdue