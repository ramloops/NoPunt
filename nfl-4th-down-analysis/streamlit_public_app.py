"""
Super Bowl LX 4th Down Analysis
================================
Robinhood-inspired Dark UI
"""

import streamlit as st
import pandas as pd

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="SB LX | 4th Down Analysis",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Robinhood-inspired CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Base dark theme - true black like Robinhood */
    .stApp {
        background: #000000;
        color: #ffffff;
    }
    
    /* Hide streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    .main .block-container {
        padding: 1.5rem 2rem;
        max-width: 1200px;
    }
    
    /* Typography - Inter like Robinhood */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Robinhood green/red */
    :root {
        --rh-green: #00C805;
        --rh-red: #FF5000;
        --rh-white: #FFFFFF;
        --rh-gray-100: #F5F5F5;
        --rh-gray-200: #E3E3E3;
        --rh-gray-400: #9B9B9B;
        --rh-gray-600: #6B6B6B;
        --rh-gray-800: #2B2B2B;
        --rh-gray-900: #1A1A1A;
        --rh-black: #000000;
    }
    
    /* Top nav bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid var(--rh-gray-800);
        margin-bottom: 2rem;
    }
    
    .nav-logo {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--rh-white);
        letter-spacing: -0.02em;
    }
    
    .nav-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8rem;
        color: var(--rh-gray-400);
    }
    
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--rh-green);
    }
    
    /* Hero section */
    .hero {
        text-align: center;
        padding: 2rem 0 3rem;
    }
    
    .hero-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--rh-gray-400);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.75rem;
    }
    
    .hero-score {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
    }
    
    .team-winner { color: var(--rh-green); }
    .team-loser { color: var(--rh-red); }
    .score-divider { color: var(--rh-gray-600); margin: 0 0.75rem; }
    
    .hero-subtitle {
        font-size: 0.9rem;
        color: var(--rh-gray-400);
        font-weight: 400;
    }
    
    /* Metric row - Robinhood style */
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1px;
        background: var(--rh-gray-800);
        border-radius: 12px;
        overflow: hidden;
        margin: 2rem 0;
    }
    
    .metric-item {
        background: var(--rh-gray-900);
        padding: 1.5rem 1rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--rh-white);
        margin-bottom: 0.25rem;
    }
    
    .metric-value.negative { color: var(--rh-red); }
    .metric-value.positive { color: var(--rh-green); }
    
    .metric-label {
        font-size: 0.7rem;
        font-weight: 500;
        color: var(--rh-gray-400);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Card component */
    .card {
        background: var(--rh-gray-900);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--rh-gray-800);
    }
    
    .card-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--rh-white);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-icon {
        width: 18px;
        height: 18px;
        opacity: 0.7;
    }
    
    .card-badge {
        font-size: 0.65rem;
        font-weight: 600;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-critical { background: rgba(255, 80, 0, 0.15); color: var(--rh-red); }
    .badge-warning { background: rgba(255, 200, 0, 0.15); color: #FFC800; }
    .badge-ok { background: rgba(0, 200, 5, 0.1); color: var(--rh-green); }
    
    /* Key play card - special styling */
    .key-play-card {
        background: linear-gradient(135deg, #1a0a0a 0%, #0d0505 100%);
        border: 1px solid rgba(255, 80, 0, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .key-play-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .key-play-icon {
        width: 20px;
        height: 20px;
        color: var(--rh-red);
    }
    
    .key-play-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--rh-red);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .key-play-situation {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--rh-white);
        margin-bottom: 0.25rem;
    }
    
    .key-play-context {
        font-size: 0.85rem;
        color: var(--rh-gray-400);
        margin-bottom: 1rem;
    }
    
    .key-play-result {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 80, 0, 0.15);
        color: var(--rh-red);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Stats grid in cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }
    
    .stat-item {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--rh-gray-800);
    }
    
    .stat-item:last-child {
        border-bottom: none;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: var(--rh-gray-400);
    }
    
    .stat-value {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--rh-white);
    }
    
    /* Chat section */
    .chat-card {
        background: var(--rh-gray-900);
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
    }
    
    .chat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .chat-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--rh-white);
    }
    
    .chat-status {
        font-size: 0.7rem;
        color: var(--rh-green);
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }
    
    /* Streamlit chat overrides */
    .stChatMessage {
        background: var(--rh-black) !important;
        border: 1px solid var(--rh-gray-800) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stChatInput > div {
        background: var(--rh-gray-900) !important;
        border: 1px solid var(--rh-gray-800) !important;
        border-radius: 8px !important;
    }
    
    .stChatInput input {
        color: var(--rh-white) !important;
        font-size: 0.9rem !important;
    }
    
    .stChatInput input::placeholder {
        color: var(--rh-gray-600) !important;
    }
    
    /* Quick action buttons */
    .quick-actions {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        background: var(--rh-black) !important;
        border: 1px solid var(--rh-gray-800) !important;
        border-radius: 20px !important;
        color: var(--rh-white) !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: var(--rh-gray-900) !important;
        border-color: var(--rh-gray-600) !important;
    }
    
    /* Tabs - Robinhood style */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        gap: 0;
        border-bottom: 1px solid var(--rh-gray-800);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--rh-gray-400) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 1rem 1.5rem !important;
        border-bottom: 2px solid transparent !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--rh-white) !important;
        border-bottom: 2px solid var(--rh-green) !important;
    }
    
    /* Data table */
    .stDataFrame {
        background: var(--rh-gray-900);
        border-radius: 8px;
        overflow: hidden;
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: var(--rh-black) !important;
    }
    
    .stDataFrame th {
        background: var(--rh-gray-900) !important;
        color: var(--rh-gray-400) !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    .stDataFrame td {
        color: var(--rh-white) !important;
        font-size: 0.85rem !important;
        border-bottom: 1px solid var(--rh-gray-800) !important;
    }
    
    /* Chart styling */
    .stLineChart, .stBarChart, .stAreaChart {
        background: var(--rh-gray-900);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Metric override */
    .stMetric {
        background: transparent !important;
        padding: 0 !important;
    }
    
    .stMetric label {
        color: var(--rh-gray-400) !important;
        font-size: 0.7rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: var(--rh-white) !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: var(--rh-red) !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: var(--rh-gray-800);
        margin: 2rem 0;
    }
    
    /* Expander */
    .stExpander {
        background: var(--rh-black);
        border: 1px solid var(--rh-gray-800);
        border-radius: 8px;
    }
    
    .stExpander header {
        color: var(--rh-white) !important;
        font-size: 0.85rem !important;
    }
    
    /* Section label */
    .section-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--rh-gray-400);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--rh-black);
        border-right: 1px solid var(--rh-gray-800);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--rh-black);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--rh-gray-800);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--rh-gray-600);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--rh-gray-600);
        font-size: 0.75rem;
        border-top: 1px solid var(--rh-gray-800);
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SNOWFLAKE CONNECTION
# ============================================
@st.cache_resource
def get_snowflake_connection():
    try:
        import snowflake.connector
        sf_config = st.secrets["snowflake"]
        conn_params = {
            "account": sf_config["account"],
            "user": sf_config["user"],
            "warehouse": sf_config["warehouse"],
            "database": sf_config["database"],
            "schema": sf_config["schema"],
        }
        
        if "private_key" in sf_config:
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import serialization
            p_key = serialization.load_pem_private_key(
                sf_config["private_key"].encode(), password=None, backend=default_backend()
            )
            conn_params["private_key"] = p_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        elif "password" in sf_config:
            conn_params["password"] = sf_config["password"]
        else:
            return None
        
        return snowflake.connector.connect(**conn_params)
    except:
        return None

# ============================================
# DATA
# ============================================
def get_fourth_down_data():
    return pd.DataFrame([
        {"QUARTER": 1, "TIME": "10:23", "YARDS_TO_GO": 8, "FIELD_POSITION": "SEA 44", 
         "NE_SCORE": 0, "SEA_SCORE": 3, "SCORE_DIFFERENTIAL": -3, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 38.0, "WPA_PCT": -3.0, "EPA": -0.5, "PUNT_ATTEMPT": 1},
        {"QUARTER": 1, "TIME": "5:45", "YARDS_TO_GO": 15, "FIELD_POSITION": "NE 35",
         "NE_SCORE": 0, "SEA_SCORE": 3, "SCORE_DIFFERENTIAL": -3, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 35.0, "WPA_PCT": -2.0, "EPA": -0.3, "PUNT_ATTEMPT": 1},
        {"QUARTER": 2, "TIME": "9:30", "YARDS_TO_GO": 17, "FIELD_POSITION": "NE 28",
         "NE_SCORE": 0, "SEA_SCORE": 6, "SCORE_DIFFERENTIAL": -6, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 25.0, "WPA_PCT": -3.0, "EPA": -0.4, "PUNT_ATTEMPT": 1},
        {"QUARTER": 2, "TIME": "2:15", "YARDS_TO_GO": 6, "FIELD_POSITION": "SEA 38",
         "NE_SCORE": 0, "SEA_SCORE": 6, "SCORE_DIFFERENTIAL": -6, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 22.0, "WPA_PCT": -2.5, "EPA": -0.6, "PUNT_ATTEMPT": 1},
        {"QUARTER": 3, "TIME": "8:40", "YARDS_TO_GO": 1, "FIELD_POSITION": "OWN 41",
         "NE_SCORE": 0, "SEA_SCORE": 12, "SCORE_DIFFERENTIAL": -12, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 12.0, "WPA_PCT": -4.2, "EPA": -0.8, "PUNT_ATTEMPT": 1},
        {"QUARTER": 3, "TIME": "2:30", "YARDS_TO_GO": 8, "FIELD_POSITION": "NE 23",
         "NE_SCORE": 0, "SEA_SCORE": 12, "SCORE_DIFFERENTIAL": -12, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 8.0, "WPA_PCT": -2.0, "EPA": -0.3, "PUNT_ATTEMPT": 1},
        {"QUARTER": 4, "TIME": "12:05", "YARDS_TO_GO": 11, "FIELD_POSITION": "NE 19",
         "NE_SCORE": 6, "SEA_SCORE": 19, "SCORE_DIFFERENTIAL": -13, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 5.0, "WPA_PCT": -1.5, "EPA": -0.2, "PUNT_ATTEMPT": 1},
        {"QUARTER": 4, "TIME": "5:20", "YARDS_TO_GO": 4, "FIELD_POSITION": "SEA 48",
         "NE_SCORE": 13, "SEA_SCORE": 22, "SCORE_DIFFERENTIAL": -9, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 6.0, "WPA_PCT": -3.0, "EPA": -0.7, "PUNT_ATTEMPT": 1},
    ])

# ============================================
# AI CHAT
# ============================================
def get_ai_response(question, fourth_downs_df):
    data_context = fourth_downs_df.to_string()
    system_prompt = f"""You are an NFL analytics expert analyzing the Patriots' 4th down decisions in Super Bowl LX (Seahawks 29, Patriots 13).

Data:
{data_context}

Key facts:
- NFL 4th & 1 conversion rate is 72%
- Patriots punted on 4th & 1 from own 41 while down 12-0 in Q3
- WPA = Win Probability Added (negative = hurt chances)
- EPA = Expected Points Added

Be concise. Reference specific plays."""

    full_prompt = f"{system_prompt}\n\nQuestion: {question}"
    
    try:
        conn = get_snowflake_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("USE ROLE SYSADMIN")
            cursor.execute(f"USE WAREHOUSE {st.secrets['snowflake']['warehouse']}")
            escaped_prompt = full_prompt.replace("'", "''")
            cursor.execute(f"SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', '{escaped_prompt}')")
            result = cursor.fetchone()
            cursor.close()
            if result and result[0]:
                return result[0]
        return "Connection error"
    except Exception as e:
        return f"Error: {str(e)[:100]}"

# ============================================
# LOAD DATA
# ============================================
fourth_downs = get_fourth_down_data()

def grade_decision(row):
    ydstogo, score_diff, wpa, punt = row['YARDS_TO_GO'], row['SCORE_DIFFERENTIAL'], row['WPA_PCT'], row['PUNT_ATTEMPT']
    if punt == 1:
        if ydstogo <= 1 and score_diff <= -10: return "CRITICAL"
        elif ydstogo <= 2 and score_diff <= -7: return "BAD"
        elif ydstogo <= 4 and score_diff <= -9: return "RISKY"
        elif wpa < -3: return "RISKY"
    return "OK"

fourth_downs['GRADE'] = fourth_downs.apply(grade_decision, axis=1)
punts = fourth_downs[fourth_downs['PUNT_ATTEMPT'] == 1]

# ============================================
# TOP NAV
# ============================================
conn = get_snowflake_connection()
st.markdown(f"""
<div class="top-nav">
    <div class="nav-logo">◆ 4TH DOWN LAB</div>
    <div class="nav-status">
        <div class="status-dot" style="background: {'#00C805' if conn else '#FF5000'}"></div>
        {'Connected' if conn else 'Offline'}
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# HERO
# ============================================
st.markdown("""
<div class="hero">
    <div class="hero-label">Super Bowl LX · February 8, 2026</div>
    <div class="hero-score">
        <span class="team-winner">SEA 29</span>
        <span class="score-divider">–</span>
        <span class="team-loser">NE 13</span>
    </div>
    <div class="hero-subtitle">New England's conservative 4th down strategy cost them the game</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# METRICS ROW
# ============================================
bad_count = len(fourth_downs[fourth_downs['GRADE'].isin(['CRITICAL', 'BAD'])])
risky_count = len(fourth_downs[fourth_downs['GRADE'] == 'RISKY'])
total_wpa = punts['WPA_PCT'].sum()
total_epa = punts['EPA'].sum()

st.markdown(f"""
<div class="metrics-row">
    <div class="metric-item">
        <div class="metric-value">{len(punts)}</div>
        <div class="metric-label">Punts on 4th</div>
    </div>
    <div class="metric-item">
        <div class="metric-value negative">{bad_count}</div>
        <div class="metric-label">Bad Calls</div>
    </div>
    <div class="metric-item">
        <div class="metric-value negative">{total_wpa:.1f}%</div>
        <div class="metric-label">Win Prob Lost</div>
    </div>
    <div class="metric-item">
        <div class="metric-value negative">{total_epa:.2f}</div>
        <div class="metric-label">Exp Points Lost</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# MAIN CONTENT
# ============================================
left_col, right_col = st.columns([1, 1], gap="large")

# LEFT: KEY PLAY
with left_col:
    st.markdown('<div class="section-label">Critical Decision</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="key-play-card">
        <div class="key-play-header">
            <svg class="key-play-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            <span class="key-play-label">Turning Point</span>
        </div>
        <div class="key-play-situation">4th & 1 at own 41</div>
        <div class="key-play-context">Q3 · 8:40 · Down 12-0</div>
        <div class="key-play-result">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
            PUNTED
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stats
    key_play = fourth_downs[fourth_downs['YARDS_TO_GO'] == 1].iloc[0]
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Win Probability", f"{key_play['WIN_PROB_PCT']:.0f}%", help="Before the punt")
        st.metric("4th & 1 Conv Rate", "72%", help="NFL average")
    with c2:
        st.metric("WPA Impact", f"{key_play['WPA_PCT']:.1f}%", delta="lost", delta_color="inverse")
        st.metric("EPA Impact", f"{key_play['EPA']:.2f}", delta="lost", delta_color="inverse")
    
    with st.expander("View Analysis"):
        st.markdown("""
        **Go for it:** 72% conversion rate means likely first down, drive continues.
        
        **If failed:** Seattle gets ball at NE 41 — not catastrophic.
        
        **Punt result:** Seattle at ~SEA 15. Net gain of 44 yards.
        
        **Verdict:** Down 12 in Q3, field position is irrelevant. You need points. Going for it was the only correct play.
        """)

# RIGHT: CHAT
with right_col:
    st.markdown('<div class="section-label">Ask the Analyst</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="chat-card">
        <div class="chat-header">
            <div class="chat-title">AI Analysis</div>
            <div class="chat-status">
                <div class="status-dot"></div>
                Cortex
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    chat_container = st.container(height=280)
    with chat_container:
        if not st.session_state.messages:
            st.markdown('<p style="color:#6B6B6B;font-size:0.85rem;text-align:center;padding:2rem;">Ask a question about the 4th down decisions</p>', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    # Quick buttons
    bc1, bc2 = st.columns(2)
    with bc1:
        if st.button("Worst decision?", use_container_width=True):
            st.session_state.pending_question = "What was the worst 4th down decision?"
    with bc2:
        if st.button("Go for it math", use_container_width=True):
            st.session_state.pending_question = "Should they have gone for it on 4th & 1?"
    
    question = st.chat_input("Ask about the game...")
    
    if "pending_question" in st.session_state:
        question = st.session_state.pending_question
        del st.session_state.pending_question
    
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner(""):
            response = get_ai_response(question, fourth_downs)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

st.markdown("---")

# ============================================
# TABS
# ============================================
tab1, tab2 = st.tabs(["All Decisions", "Win Probability"])

with tab1:
    display_df = fourth_downs.copy()
    display_df['QTR'] = display_df['QUARTER'].apply(lambda x: f"Q{x}")
    display_df['SITUATION'] = display_df['YARDS_TO_GO'].apply(lambda x: f"4th & {x}")
    display_df['SCORE'] = display_df.apply(lambda r: f"{int(r['NE_SCORE'])}-{int(r['SEA_SCORE'])}", axis=1)
    display_df['WIN%'] = display_df['WIN_PROB_PCT'].apply(lambda x: f"{x:.0f}%")
    display_df['WPA'] = display_df['WPA_PCT'].apply(lambda x: f"{x:+.1f}%")
    
    # Grade symbols (monochrome)
    def grade_symbol(g):
        if g == "CRITICAL": return "●"  # filled circle
        if g == "BAD": return "●"
        if g == "RISKY": return "◐"  # half circle
        return "○"  # empty circle
    
    display_df['◆'] = display_df['GRADE'].apply(grade_symbol)
    
    st.dataframe(
        display_df[['◆', 'QTR', 'TIME', 'SITUATION', 'FIELD_POSITION', 'SCORE', 'WIN%', 'WPA', 'GRADE']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "◆": st.column_config.TextColumn("", width="small"),
            "GRADE": st.column_config.TextColumn("Grade", width="small"),
        }
    )
    
    st.caption("● Critical/Bad | ◐ Risky | ○ Acceptable")

with tab2:
    st.markdown('<div class="section-label">Win Probability by Play</div>', unsafe_allow_html=True)
    
    chart_df = fourth_downs[['WIN_PROB_PCT']].copy()
    chart_df.index = range(1, len(chart_df) + 1)
    chart_df.columns = ['Win %']
    
    st.area_chart(chart_df, color="#FF5000", use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Start", "38%")
    with col2:
        st.metric("End", "6%")
    with col3:
        st.metric("Lost", f"{abs(total_wpa):.1f}%")
    
    st.caption("Each conservative punt eroded New England's chances until victory was impossible.")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    Data: nflfastR · AI: Snowflake Cortex · Levi's Stadium, Santa Clara
</div>
""", unsafe_allow_html=True)
