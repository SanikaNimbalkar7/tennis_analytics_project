import pyodbc
import json

# Connect to SQL Server
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=YOUR_SERVER_NAME;"   # e.g., localhost\SQLEXPRESS
    "DATABASE=tennis_analytics;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

# ----------------- INSERT CATEGORIES -----------------
with open("competitions.json") as f:
    data = json.load(f)

categories = data.get("categories", [])
for cat in categories:
    cursor.execute(
        "INSERT INTO Categories (category_name) VALUES (?)",
        cat["name"]
    )
conn.commit()
print("✅ Categories inserted")

# ----------------- INSERT COMPETITIONS -----------------
competitions = data.get("competitions", [])
for comp in competitions:
    cursor.execute(
        "INSERT INTO Competitions (competition_name, category_id, type, gender) VALUES (?, ?, ?, ?)",
        comp["name"], comp["category_id"], comp["type"], comp["gender"]
    )
conn.commit()
print("✅ Competitions inserted")

# ----------------- INSERT COMPLEXES & VENUES -----------------
with open("complexes.json") as f:
    complex_data = json.load(f)

complexes = complex_data.get("complexes", [])
venues = complex_data.get("venues", [])

for compx in complexes:
    cursor.execute(
        "INSERT INTO Complexes (complex_name) VALUES (?)",
        compx["name"]
    )
conn.commit()
print("✅ Complexes inserted")

for venue in venues:
    cursor.execute(
        "INSERT INTO Venues (venue_name, city_name, country_name, timezone, complex_id) VALUES (?, ?, ?, ?, ?)",
        venue["name"], venue["city"], venue["country"], venue["timezone"], venue["complex_id"]
    )
conn.commit()
print("✅ Venues inserted")

# ----------------- INSERT COMPETITORS & RANKINGS -----------------
with open("doubles_rankings.json") as f:
    ranking_data = json.load(f)

competitors = ranking_data.get("competitors", [])
rankings = ranking_data.get("rankings", [])

for comp in competitors:
    cursor.execute(
        "INSERT INTO Competitors (name, country, country_code) VALUES (?, ?, ?)",
        comp["name"], comp["country"], comp["country_code"]
    )
conn.commit()
print("✅ Competitors inserted")

for rank in rankings:
    cursor.execute(
        "INSERT INTO Competitor_Rankings (competitor_id, rank, movement, points) VALUES (?, ?, ?, ?)",
        rank["competitor_id"], rank["rank"], rank["movement"], rank["points"]
    )
conn.commit()
print("✅ Competitor Rankings inserted")

conn.close()
print("🎉 Database populated successfully!")
