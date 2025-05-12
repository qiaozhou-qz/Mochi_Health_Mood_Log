import streamlit as st
from datetime import datetime, date
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET_NAME = "mood_of_the_queue"
SPREADSHEET = GSPREAD_CLIENT.open(SHEET_NAME)

# App title and description
st.title("🎭 Mood of the Queue")
st.markdown("Track the emotional vibe of patient support tickets throughout the day.")

# Initialize Google Sheet if it doesn't exist
def init_sheet():
    try:
        worksheet = SPREADSHEET.worksheet("Mood Log")
    except:
        worksheet = SPREADSHEET.add_worksheet(title="Mood Log", rows=1000, cols=3)
        worksheet.append_row(["Timestamp", "Mood", "Note"])
    return worksheet

worksheet = init_sheet()

# Mood options with emojis
MOOD_OPTIONS = {
    "😊 Happy": "happy",
    "😐 Neutral": "neutral",
    "😠 Frustrated": "frustrated",
    "😕 Confused": "confused",
    "😟 Anxious": "anxious"
}

# Log mood form
with st.form("mood_form"):
    st.subheader("Log Current Mood")
    mood = st.radio("Select mood:", list(MOOD_OPTIONS.keys()))
    note = st.text_input("Optional note:")
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mood_value = MOOD_OPTIONS[mood]
        worksheet.append_row([timestamp, mood_value, note])
        st.success("Mood logged successfully!")

# Visualization section
st.subheader("Today's Mood Trends")

@st.cache_data(ttl=5)  # Auto-refresh every 5 seconds
def get_today_data():
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)
    if not df.empty:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df["Date"] = df["Timestamp"].dt.date
        today = date.today()
        return df[df["Date"] == today]
    return pd.DataFrame()

today_data = get_today_data()

if not today_data.empty:
    # Mood count bar chart
    mood_counts = today_data["Mood"].value_counts().reset_index()
    mood_counts.columns = ["Mood", "Count"]
    
    fig = px.bar(
        mood_counts,
        x="Mood",
        y="Count",
        color="Mood",
        title=f"Mood Distribution for {date.today().strftime('%Y-%m-%d')}",
        labels={"Count": "Number of Logs"},
        color_discrete_map={
            "happy": "#2ecc71",
            "neutral": "#f39c12",
            "frustrated": "#e74c3c",
            "confused": "#3498db",
            "anxious": "#9b59b6"
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show recent logs
    st.subheader("Recent Logs")
    today_data_sorted = today_data.sort_values("Timestamp", ascending=False)
    st.dataframe(today_data_sorted[["Timestamp", "Mood", "Note"]].head(5))
else:
    st.info("No mood logs for today yet. Add your first log above!")
