import streamlit as st
import pandas as pd

st.set_page_config(page_title="Super Bowl LX: 4th Down Analysis", page_icon="🏈", layout="wide")

# Data
fourth_downs = pd.DataFrame([
    {"QUARTER": 1, "TIME": "10:23", "YARDS_TO_GO": 8, "FIELD_POSITION": "SEA 44", 
     "NE_SCORE": 0, "SEA_SCORE": 3, "SCORE_DIFF": -3, "WIN_PROB": 38.0, "WPA": -3.0, "EPA": -0.5, "PUNT": 1},
    {"QUARTER": 1, "TIME": "5:45", "YARDS_TO_GO": 15, "FIELD_POSITION": "NE 35",
     "NE_SCORE": 0, "SEA_SCORE": 3, "SCORE_DIFF": -3, "WIN_PROB": 35.0, "WPA": -2.0, "EPA": -0.3, "PUNT": 1},
    {"QUARTER": 2, "TIME": "9:30", "YARDS_TO_GO": 17, "FIELD_POSITION": "NE 28",
     "NE_SCORE": 0, "SEA_SCORE": 6, "SCORE_DIFF": -6, "WIN_PROB": 25.0, "WPA": -3.0, "EPA": -0.4, "PUNT": 1},
    {"QUARTER": 2, "TIME": "2:15", "YARDS_TO_GO": 6, "FIELD_POSITION": "SEA 38",
     "NE_SCORE": 0, "SEA_SCORE": 6, "SCORE_DIFF": -6, "WIN_PROB": 22.0, "WPA": -2.5, "EPA": -0.6, "PUNT": 1},
    {"QUARTER": 3, "TIME": "8:40", "YARDS_TO_GO": 1, "FIELD_POSITION": "OWN 41",
     "NE_SCORE": 0, "SEA_SCORE": 12, "SCORE_DIFF": -12, "WIN_PROB": 12.0, "WPA": -4.2, "EPA": -0.8, "PUNT": 1},
    {"QUARTER": 3, "TIME": "2:30", "YARDS_TO_GO": 8, "FIELD_POSITION": "NE 23",
     "NE_SCORE": 0, "SEA_SCORE": 12, "SCORE_DIFF": -12, "WIN_PROB": 8.0, "WPA": -2.0, "EPA": -0.3, "PUNT": 1},
    {"QUARTER": 4, "TIME": "12:05", "YARDS_TO_GO": 11, "FIELD_POSITION": "NE 19",
     "NE_SCORE": 6, "SEA_SCORE": 19, "SCORE_DIFF": -13, "WIN_PROB": 5.0, "WPA": -1.5, "EPA": -0.2, "PUNT": 1},
    {"QUARTER": 4, "TIME": "5:20", "YARDS_TO_GO": 4, "FIELD_POSITION": "SEA 48",
     "NE_SCORE": 13, "SEA_SCORE": 22, "SCORE_DIFF": -9, "WIN_PROB": 6.0, "WPA": -3.0, "EPA": -0.7, "PUNT": 1},
])

def grade(row):
    if row["PUNT"] == 1:
        if row["YARDS_TO_GO"] <= 1 and row["SCORE_DIFF"] <= -10:
            return "🔴 TERRIBLE"
        elif row["YARDS_TO_GO"] <= 2 and row["SCORE_DIFF"] <= -7:
            return "🔴 BAD"
        elif row["WPA"] < -2.5:
            return "🟡 QUESTIONABLE"
    return "✅ OK"

fourth_downs["GRADE"] = fourth_downs.apply(grade, axis=1)

# Header
st.title("🏈 Super Bowl LX: 4th Down Analysis")
st.markdown("### Seahawks 29 - Patriots 13")

# Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("4th Down Punts", len(fourth_downs))
c2.metric("Bad Decisions", len(fourth_downs[fourth_downs["GRADE"].str.contains("🔴")]))
c3.metric("Total WPA Lost", f"{fourth_downs['WPA'].sum():.1f}%")
c4.metric("Total EPA Lost", f"{fourth_downs['EPA'].sum():.2f}")

st.markdown("---")

# Key Play
st.subheader("🔥 THE KEY PLAY: 4th & 1, down 12-0, Q3")
col1, col2 = st.columns(2)

with col1:
    st.error("**Decision: PUNT** 👎")
    st.metric("Field Position", "Own 41-yard line")
    st.metric("Win Probability", "12%")
    st.metric("WPA from Punt", "-4.2%")

with col2:
    st.markdown("### Why This Was Wrong")
    st.markdown("""
    - **NFL 4th & 1 conversion rate: 72%**
    - If convert: Keep driving, WP goes UP
    - If fail: SEA ball at NE 41 (not much worse than punt)
    - Punt: Gave up without a fight
    
    **Expected value clearly favored going for it!**
    """)

st.markdown("---")

# All plays table
st.subheader("📊 All 4th Down Decisions")

display = fourth_downs.copy()
display["SITUATION"] = "Q" + display["QUARTER"].astype(str) + " " + display["TIME"]
display["4TH &"] = display["YARDS_TO_GO"]
display["SCORE"] = display["NE_SCORE"].astype(str) + "-" + display["SEA_SCORE"].astype(str)

st.dataframe(
    display[["SITUATION", "4TH &", "FIELD_POSITION", "SCORE", "WIN_PROB", "WPA", "EPA", "GRADE"]],
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# Chart
st.subheader("📉 Win Probability Dropped With Each Punt")
chart_data = fourth_downs.copy()
chart_data["Play"] = range(1, len(chart_data) + 1)
st.bar_chart(chart_data.set_index("Play")["WIN_PROB"])

# Sidebar
with st.sidebar:
    st.header("Super Bowl LX")
    st.markdown("🦅 Seahawks **29**")
    st.markdown("🏈 Patriots **13**")
    st.markdown("---")
    st.markdown("📅 Feb 8, 2026")
    st.markdown("🏟️ Levi's Stadium")
    st.markdown("---")
    st.caption("Data: nflfastR")