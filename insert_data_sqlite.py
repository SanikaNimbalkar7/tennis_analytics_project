import sqlite3
import json

conn = sqlite3.connect("tennis_analytics.db")
cursor = conn.cursor()

# Load Competitors JSON
with open("competitors.json") as f:
    competitors = json.load(f)

for comp in competitors:
    cursor.execute("""
        INSERT INTO Competitors (name, country, country_code) VALUES (?, ?, ?)
    """, (comp["name"], comp["country"], comp["country_code"]))

# Load Competitor Rankings JSON
with open("rankings_doubles.json") as f:
    rankings = json.load(f)

for r in rankings:
    cursor.execute("""
        INSERT INTO Competitor_Rankings (competitor_id, rank, movement, points) VALUES (?, ?, ?, ?)
    """, (r["competitor_id"], r["rank"], r["movement"], r["points"]))

conn.commit()
conn.close()
print("Data inserted successfully.")
