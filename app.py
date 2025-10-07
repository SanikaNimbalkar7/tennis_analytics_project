# app.py
import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🎾 Tennis Analytics Dashboard", layout="wide")

# ----------------- DATABASE CONNECTION -----------------
def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",  # Replace with your MySQL password
        database="tennis_analytics"
    )
    return conn

def fetch_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ----------------- SIDEBAR -----------------
st.sidebar.title("Tennis Analytics")
menu = st.sidebar.radio("Navigate", ["Dashboard", "Competitor Search", "Country Analysis", "Leaderboards"])

# ----------------- DASHBOARD -----------------
if menu == "Dashboard":
    st.title("🎾 Tennis Analytics Dashboard")

    # Key Metrics
    total_comp = fetch_data("SELECT COUNT(*) as total FROM Competitors")["total"][0]
    total_countries = fetch_data("SELECT COUNT(DISTINCT country) as total FROM Competitors")["total"][0]
    highest_points = fetch_data("SELECT MAX(points) as max_points FROM Competitor_Rankings")["max_points"][0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", total_comp)
    col2.metric("Countries Represented", total_countries)
    col3.metric("Highest Points Scored", highest_points)

    st.markdown("---")
    st.subheader("Competitions Overview")
    competitions = fetch_data("""
        SELECT comp.competition_name, cat.category_name, comp.type, comp.gender
        FROM Competitions comp
        JOIN Categories cat ON comp.category_id = cat.category_id
    """)
    st.dataframe(competitions)

# ----------------- COMPETITOR SEARCH -----------------
elif menu == "Competitor Search":
    st.title("🔍 Competitor Search & Filter")

    # Search by name
    name = st.text_input("Search Competitor by Name")
    query = "SELECT c.name, c.country, r.rank, r.points FROM Competitors c JOIN Competitor_Rankings r ON c.competitor_id=r.competitor_id WHERE 1=1"
    if name:
        query += f" AND c.name LIKE '%{name}%'"

    # Filter by country
    countries = ["All"] + list(fetch_data("SELECT DISTINCT country FROM Competitors")["country"])
    country_filter = st.selectbox("Filter by Country", countries)
    if country_filter != "All":
        query += f" AND c.country='{country_filter}'"

    # Filter by rank range
    rank_min, rank_max = st.slider("Rank Range", 1, 100, (1, 10))
    query += f" AND r.rank BETWEEN {rank_min} AND {rank_max}"

    df = fetch_data(query)
    st.dataframe(df)

# ----------------- COUNTRY-WISE ANALYSIS -----------------
elif menu == "Country Analysis":
    st.title("🌍 Country-wise Analysis")

    df_country = fetch_data("""
        SELECT c.country, COUNT(*) as total_competitors, AVG(r.points) as avg_points
        FROM Competitors c
        JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
        GROUP BY c.country
        ORDER BY total_competitors DESC
    """)
    st.dataframe(df_country)

    # Total competitors by country
    st.subheader("Competitors by Country")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x="country", y="total_competitors", data=df_country, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Average points by country
    st.subheader("Average Points by Country")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    sns.barplot(x="country", y="avg_points", data=df_country, ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# ----------------- LEADERBOARDS -----------------
elif menu == "Leaderboards":
    st.title("🏆 Leaderboards")

    st.subheader("Top 5 Ranked Competitors")
    top5_ranked = fetch_data("""
        SELECT c.name, c.country, r.rank, r.points
        FROM Competitors c
        JOIN Competitor_Rankings r ON c.competitor_id=r.competitor_id
        ORDER BY r.rank ASC
        LIMIT 5
    """)
    st.table(top5_ranked)

    st.subheader("Top 5 Competitors by Points")
    top5_points = fetch_data("""
        SELECT c.name, c.country, r.rank, r.points
        FROM Competitors c
        JOIN Competitor_Rankings r ON c.competitor_id=r.competitor_id
        ORDER BY r.points DESC
        LIMIT 5
    """)
    st.table(top5_points)
