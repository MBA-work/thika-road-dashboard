import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Thika Road Traffic Dashboard", layout="wide")

st.title("🚗 Thika Road Traffic Dashboard: Personal Cars vs. Matatus")
st.markdown("An interactive breakdown of vehicles passing along Thika Superhighway on a Random day.")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("traffic_data.csv")

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔎Filter Options")

# Direction Filter (Inbound / Outbound)
directions_available = list(df["Direction"].unique())
selected_direction = st.sidebar.multiselect(
    "Select Direction:",
    options=directions_available,
    default=directions_available # Pre-selects all choices by default
)

# Time of Day Filter
times_available = list(df["Time_of_Day"].unique())
selected_time = st.sidebar.multiselect(
    "Select Time of Day:",
    options=times_available,
    default=times_available # Pre-selects all choices by default
)

# Filter Dataframe based on selections
filtered_df = df[
    (df["Direction"].isin(selected_direction)) & 
    (df["Time_of_Day"].isin(selected_time))
]

# --- KEY METRICS ---
col1, col2 = st.columns(2)
total_cars = filtered_df[filtered_df["Vehicle_Type"] == "Personal Cars"]["Count"].sum()
total_matatus = filtered_df[filtered_df["Vehicle_Type"] == "Matatus"]["Count"].sum()

col1.metric("Total Personal Cars", f"{total_cars:,}")
col2.metric("Total Matatus", f"{total_matatus:,}")

st.markdown("---")

# --- VISUALIZATIONS ---
if not filtered_df.empty:
    fig_bar = px.bar(
        filtered_df,
        x="Time_of_Day",
        y="Count",
        color="Vehicle_Type",
        barmode="group",
        title="Vehicle Volume by Time of Day",
        labels={"Count": "Vehicle Count", "Time_of_Day": "Time Period"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_pie = px.pie(
        filtered_df,
        names="Vehicle_Type",
        values="Count",
        title="Total Modal Share (Cars vs Matatus)"
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.warning("No data available for the selected filters. Please select at least one option in the sidebar.")
