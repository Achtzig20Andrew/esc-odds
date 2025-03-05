import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from sqlalchemy import create_engine
import random
import os

# Database connection
DB_HOST = "your_db_host"
DB_NAME = "esc_odds"
DB_USER = "esc_odds_user"
DB_PASS = "your_db_password"

print(f"======= DB_URL ====== {os.environ["DB_URL"]}")

def get_data():
    """Fetch ranking data from the PostgreSQL database."""
    engine = create_engine(os.environ["DB_URL"])
    query = """
    SELECT "country", "date", "rank", "winningChance" FROM "rankings_table"
    ORDER BY date;
    """
    df = pd.read_sql(query, engine)
    return df


def get_example_data():
    """Generate example ranking data."""
    dates = pd.date_range(start="2024-01-01", end="2024-06-01", freq="D")
    countries = ["USA", "Germany", "France", "Japan", "India"]
    data = []

    for country in countries:
        rank = random.randint(1, 10)
        for date in dates:
            if random.random() > 0.1:  # Simulate some missing values
                rank = max(1, min(10, rank + random.randint(-1, 1)))
                data.append({"country": country, "date": date, "rank": rank})

    return pd.DataFrame(data)


# Fetch example data
# df = get_example_data()


# Fetch data
df = get_data()

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Streamlit UI
st.title("ESC Odds over time")
st.write(
    "This chart shows the ranking positions and winning probabilities of the countries over time."
)

# Select countries
default_countries = df["country"].unique()[:5]
selected_countries = st.multiselect(
    "Select countries", df["country"].unique(), default=default_countries
)

# Filter data
df_filtered = df[df["country"].isin(selected_countries)]

# Plot data
fig1 = px.line(
    df_filtered,
    x="date",
    y="rank",
    color="country",
    markers=True,
    title="Position",
    labels={"rank": "Position", "date": "Date"},
    line_shape="linear",
)
fig1.update_yaxes(
    autorange="reversed"
)  # Since ranking positions typically have lower numbers as better ranks

# Plot second diagram
fig2 = px.line(
    df_filtered,
    x="date",
    y="winningChance",
    color="country",
    markers=True,
    title="Winning probability over time",
    labels={"winningChance": "%", "date": "Date"},
    line_shape="linear",
)
fig2.update_yaxes()


st.plotly_chart(fig1)
st.plotly_chart(fig2)
