# create_sqlite_db.py
import sqlite3

conn = sqlite3.connect("tennis_analytics.db")
cursor = conn.cursor()

# Categories Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT
)
""")

# Competitions Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Competitions (
    competition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_name TEXT,
    category_id INTEGER,
    type TEXT,
    gender TEXT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
)
""")

# Competitors Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Competitors (
    competitor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    country TEXT,
    country_code TEXT
)
""")

# Competitor Rankings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Competitor_Rankings (
    rank_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_id INTEGER,
    rank INTEGER,
    movement TEXT,
    points INTEGER,
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
)
""")

# Complexes Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Complexes (
    complex_id INTEGER PRIMARY KEY AUTOINCREMENT,
    complex_name TEXT
)
""")

# Venues Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Venues (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name TEXT,
    city_name TEXT,
    country_name TEXT,
    timezone TEXT,
    complex_id INTEGER,
    FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
)
""")

conn.commit()
conn.close()
print("SQLite database and tables created successfully.")
