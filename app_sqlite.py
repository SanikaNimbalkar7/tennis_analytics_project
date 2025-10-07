# app_sqlite.py
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🎾 Tennis Analytics Dashboard", layout="wide")

# ----------------- DATABASE CONNECTION -----------------
def get_connection():
    try:
        conn = sqlite3.connect("tennis_analytics.db")
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

def fetch_data(query, fallback_df=None):
    conn = get_connection()
    if conn:
        try:
            df = pd.read_sql_query(query, conn)
            conn.close()
            if df.empty and fallback_df is not None:
                return fallback_df
            return df
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            conn.close()
            if fallback_df is not None:
                return fallback_df
            return pd.DataFrame()
    else:
        return fallback_df if fallback_df is not None else pd.DataFrame()

# ----------------- SIDEBAR -----------------
st.sidebar.title("🎾 Tennis Analytics")
menu = st.sidebar.radio("Navigate", ["Dashboard", "Competitor Search", "Country Analysis", "Leaderboards"])

# ----------------- Fallback Dummy Data -----------------
dummy_competitors = pd.DataFrame({
    "name": ["Roger Federer", "Rafael Nadal", "Novak Djokovic"],
    "country": ["Switzerland", "Spain", "Serbia"],
    "rank": [1, 2, 3],
    "points": [12000, 11000, 10500]
})

dummy_countries = pd.DataFrame({
    "country": ["Switzerland", "Spain", "Serbia"],
    "total_competitors": [1,1,1],
    "avg_points": [12000, 11000, 10500]
})

dummy_competitions = pd.DataFrame({
    "competition_name": ["Wimbledon", "US Open"],
    "category_name": ["Grand Slam", "Grand Slam"],
    "type": ["Singles", "Singles"],
    "gender": ["Men", "Men"]
})

# ----------------- DASHBOARD -----------------
if menu == "Dashboard":
    st.title("🎾 Tennis Analytics Dashboard")

    total_comp = fetch_data("SELECT COUNT(*) as total FROM Competitors", fallback_df=pd.DataFrame({"total":[3]}))
    total_countries = fetch_data("SELECT COUNT(DISTINCT country) as total FROM Competitors", fallback_df=pd.DataFrame({"total":[3]}))
    highest_points = fetch_data("SELECT MAX(points) as max_points FROM Competitor_Rankings", fallback_df=pd.DataFrame({"max_points":[12000]}))

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", total_comp["total"][0])
    col2.metric("Countries Represented", total_countries["total"][0])
    col3.metric("Highest Points Scored", highest_points["max_points"][0])

    st.markdown("---")
    st.subheader("Competitions Overview")
    competitions = fetch_data("""
        SELECT comp.competition_name, cat.category_name, comp.type, comp.gender
        FROM Competitions comp
        JOIN Categories cat ON comp.category_id = cat.category_id
    """, fallback_df=dummy_competitions)
    st.dataframe(competitions)

# ----------------- COMPETITOR SEARCH -----------------
elif menu == "Competitor Search":
    st.title("🔍 Competitor Search & Filter")

    name = st.text_input("Search Competitor by Name")
    countries = fetch_data("SELECT DISTINCT country FROM Competitors", fallback_df=dummy_competitors)["country"].tolist()
    countries = ["All"] + countries
    country_filter = st.selectbox("Filter by Country", countries)
    rank_min, rank_max = st.slider("Rank Range", 1, 100, (1, 10))

    query = "SELECT c.name, c.country, r.rank, r.points FROM Competitors c JOIN Competitor_Rankings r ON c.competitor_id=r.competitor_id WHERE 1=1"
    if name:
        query += f" AND c.name LIKE '%{name}%'"
    if country_filter != "All":
        query += f" AND c.country='{country_filter}'"
    query += f" AND r.rank BETWEEN {rank_min} AND {rank_max}"

    df = fetch_data(query, fallback_df=dummy_competitors)
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
    """, fallback_df=dummy_countries)

    st.dataframe(df_country)

    st.subheader("Competitors by Country")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x="country", y="total_competitors", data=df_country, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Average Points by Country")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    sns.barplot(x="country", y="avg_points", data=df_country, ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# ----------------- LEADERBOARDS -----------------
elif menu == "Leaderboards":
    st.title("🏆 Leaderboards")

    top5_ranked = fetch_data("""
        SELECT c.name, c.country, r.rank, r.points
        FROM Competitors c
        JOIN Competitor_Rankings r ON c.competitor_id=r.competitor_id
        ORDER BY r.rank ASC
        LIMIT 5
    """, fallback_df=dummy_competitors)
    st.subheader("Top 5 Ranked Competitors")
    st.table(top5_ranked)

    top5_points = fetch_data("""
        SELECT c.name, c.country, r.rank, r.points
        FROM Competitors c
        JOIN Competitor_Rankings r ON c.competitor_id=r.competitor_id
        ORDER BY r.points DESC
        LIMIT 5
    """, fallback_df=dummy_competitors)
    st.subheader("Top 5 Competitors by Points")
    st.table(top5_points)
