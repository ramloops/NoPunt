"""
Super Bowl LX 4th Down Analysis
================================
Dark Pro Theme | NNG Standards
"""

import streamlit as st
import pandas as pd

# ============================================
# PAGE CONFIG & DARK THEME
# ============================================
st.set_page_config(
    page_title="SB LX | 4th Down Analysis",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Dark Pro Theme
st.markdown("""
<style>
    /* Import clean fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Dark theme base */
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #111118 50%, #0d0d12 100%);
    }
    
    /* Hide default header */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Main container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Typography */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    p, span, div, .stMarkdown {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Hero title styling */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff4444 0%, #ff6b6b 50%, #ffa500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: #888;
        font-weight: 400;
        margin-top: 0.5rem;
    }
    
    .score-display {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #fff;
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        border: 1px solid #2a2a4a;
        display: inline-block;
        margin: 1rem 0;
    }
    
    .team-sea { color: #69BE28; }
    .team-ne { color: #c60c30; }
    .score-sep { color: #444; margin: 0 0.5rem; }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #0f0f1a 100%);
        border: 1px solid #2a2a4a;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #ff4444;
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(255, 68, 68, 0.15);
    }
    
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #fff;
    }
    
    .metric-value.bad { color: #ff4444; }
    .metric-value.warn { color: #ffa500; }
    .metric-value.good { color: #00ff88; }
    
    .metric-label {
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.5rem;
    }
    
    /* Key play alert box */
    .key-play-box {
        background: linear-gradient(135deg, #2d1f1f 0%, #1a1215 100%);
        border: 2px solid #ff4444;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .key-play-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #ff4444, #ff6b6b, #ffa500);
    }
    
    .key-play-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.8rem;
        color: #ff6b6b;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.5rem;
    }
    
    .key-play-situation {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    
    .key-play-result {
        font-size: 1.2rem;
        color: #ff4444;
        font-weight: 600;
    }
    
    /* Chat container */
    .chat-container {
        background: linear-gradient(145deg, #12121a 0%, #0a0a0f 100%);
        border: 1px solid #1a1a2a;
        border-radius: 16px;
        padding: 1.5rem;
        min-height: 400px;
    }
    
    /* Streamlit overrides */
    .stMetric {
        background: linear-gradient(145deg, #1a1a2e 0%, #0f0f1a 100%);
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stMetric label {
        color: #666 !important;
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.8rem !important;
        color: #fff !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4a 100%);
        border: 1px solid #3a3a5a;
        border-radius: 8px;
        color: #fff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2a2a4a 0%, #3a3a5a 100%);
        border-color: #ff4444;
        transform: translateY(-1px);
    }
    
    /* Chat input */
    .stChatInput > div {
        background: #1a1a2e !important;
        border: 1px solid #2a2a4a !important;
        border-radius: 12px !important;
    }
    
    .stChatInput input {
        color: #fff !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: #12121a !important;
        border: 1px solid #1a1a2a !important;
        border-radius: 12px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #0a0a0f;
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #666;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #2a2a4a 100%);
        color: #fff;
    }
    
    /* Data table */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: #0a0a0f;
        border: 1px solid #1a1a2a;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #2a2a4a, transparent);
        margin: 2rem 0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0f 0%, #111118 100%);
        border-right: 1px solid #1a1a2a;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1a1a2a;
    }
    
    /* Status indicator */
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-dot.connected { background: #00ff88; box-shadow: 0 0 8px #00ff88; }
    .status-dot.disconnected { background: #ff4444; }
    
    /* Analysis cards */
    .analysis-stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid #1a1a2a;
    }
    
    .analysis-stat:last-child {
        border-bottom: none;
    }
    
    .stat-label {
        color: #888;
        font-size: 0.85rem;
    }
    
    .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        color: #fff;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #444;
        font-size: 0.75rem;
        padding: 2rem 0 1rem;
        border-top: 1px solid #1a1a2a;
        margin-top: 3rem;
    }
    
    .footer a {
        color: #666;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SNOWFLAKE CONNECTION
# ============================================
@st.cache_resource
def get_snowflake_connection():
    """Create Snowflake connection from secrets"""
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
                sf_config["private_key"].encode(),
                password=None,
                backend=default_backend()
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
        
    except Exception as e:
        return None

# ============================================
# DATA
# ============================================
def get_fourth_down_data():
    """Patriots 4th down data from Super Bowl LX"""
    return pd.DataFrame([
        {"QUARTER": 1, "TIME": "10:23", "YARDS_TO_GO": 8, "FIELD_POSITION": "SEA 44", 
         "NE_SCORE": 0, "SEA_SCORE": 3, "SCORE_DIFFERENTIAL": -3, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 38.0, "WPA_PCT": -3.0, "EPA": -0.5, "PUNT_ATTEMPT": 1,
         "PLAY_DESCRIPTION": "Punt to SEA 20"},
        {"QUARTER": 1, "TIME": "5:45", "YARDS_TO_GO": 15, "FIELD_POSITION": "NE 35",
         "NE_SCORE": 0, "SEA_SCORE": 3, "SCORE_DIFFERENTIAL": -3, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 35.0, "WPA_PCT": -2.0, "EPA": -0.3, "PUNT_ATTEMPT": 1,
         "PLAY_DESCRIPTION": "Punt downed at SEA 15"},
        {"QUARTER": 2, "TIME": "9:30", "YARDS_TO_GO": 17, "FIELD_POSITION": "NE 28",
         "NE_SCORE": 0, "SEA_SCORE": 6, "SCORE_DIFFERENTIAL": -6, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 25.0, "WPA_PCT": -3.0, "EPA": -0.4, "PUNT_ATTEMPT": 1,
         "PLAY_DESCRIPTION": "Punt to SEA 25"},
        {"QUARTER": 2, "TIME": "2:15", "YARDS_TO_GO": 6, "FIELD_POSITION": "SEA 38",
         "NE_SCORE": 0, "SEA_SCORE": 6, "SCORE_DIFFERENTIAL": -6, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 22.0, "WPA_PCT": -2.5, "EPA": -0.6, "PUNT_ATTEMPT": 1,
         "PLAY_DESCRIPTION": "Punt into end zone, touchback"},
        {"QUARTER": 3, "TIME": "8:40", "YARDS_TO_GO": 1, "FIELD_POSITION": "OWN 41",
         "NE_SCORE": 0, "SEA_SCORE": 12, "SCORE_DIFFERENTIAL": -12, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 12.0, "WPA_PCT": -4.2, "EPA": -0.8, "PUNT_ATTEMPT": 1,
         "PLAY_DESCRIPTION": "4th & 1 PUNT from own 41 - THE KEY PLAY"},
        {"QUARTER": 3, "TIME": "2:30", "YARDS_TO_GO": 8, "FIELD_POSITION": "NE 23",
         "NE_SCORE": 0, "SEA_SCORE": 12, "SCORE_DIFFERENTIAL": -12, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 8.0, "WPA_PCT": -2.0, "EPA": -0.3, "PUNT_ATTEMPT": 1,
         "PLAY_DESCRIPTION": "Punt to SEA 45"},
        {"QUARTER": 4, "TIME": "12:05", "YARDS_TO_GO": 11, "FIELD_POSITION": "NE 19",
         "NE_SCORE": 6, "SEA_SCORE": 19, "SCORE_DIFFERENTIAL": -13, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 5.0, "WPA_PCT": -1.5, "EPA": -0.2, "PUNT_ATTEMPT": 1,
         "PLAY_DESCRIPTION": "Punt to SEA 35"},
        {"QUARTER": 4, "TIME": "5:20", "YARDS_TO_GO": 4, "FIELD_POSITION": "SEA 48",
         "NE_SCORE": 13, "SEA_SCORE": 22, "SCORE_DIFFERENTIAL": -9, "PLAY_TYPE": "punt",
         "WIN_PROB_PCT": 6.0, "WPA_PCT": -3.0, "EPA": -0.7, "PUNT_ATTEMPT": 1,
         "PLAY_DESCRIPTION": "Punt with 5 min left, down 9"},
    ])

# ============================================
# AI CHAT - SNOWFLAKE CORTEX
# ============================================
def get_ai_response(question, fourth_downs_df):
    """Get AI response using Snowflake Cortex"""
    data_context = fourth_downs_df.to_string()
    
    system_prompt = f"""You are an NFL analytics expert analyzing the Patriots' 4th down decisions in Super Bowl LX (Seahawks 29, Patriots 13).

Here is the data on all Patriots 4th down plays:
{data_context}

Key facts:
- NFL 4th & 1 conversion rate is 72%
- The Patriots punted on 4th & 1 from their own 41 while down 12-0 in Q3
- WPA = Win Probability Added (negative means the decision hurt their chances)
- EPA = Expected Points Added

Answer questions concisely and reference specific plays from the data."""

    full_prompt = f"{system_prompt}\n\nUser question: {question}"
    
    try:
        conn = get_snowflake_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("USE ROLE SYSADMIN")
            cursor.execute(f"USE WAREHOUSE {st.secrets['snowflake']['warehouse']}")
            
            escaped_prompt = full_prompt.replace("'", "''")
            sql = f"""SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', '{escaped_prompt}') as response"""
            
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
            
            if result and result[0]:
                return result[0]
            return "No response from Cortex"
                
    except Exception as e:
        return f"Error: {str(e)[:150]}"

# ============================================
# LOAD & PROCESS DATA
# ============================================
fourth_downs = get_fourth_down_data()

def grade_decision(row):
    ydstogo = row.get('YARDS_TO_GO', 10)
    score_diff = row.get('SCORE_DIFFERENTIAL', 0)
    wpa = row.get('WPA_PCT', 0)
    punt = row.get('PUNT_ATTEMPT', 0)
    
    if punt == 1:
        if ydstogo <= 1 and score_diff <= -10:
            return "TERRIBLE"
        elif ydstogo <= 2 and score_diff <= -7:
            return "BAD"
        elif ydstogo <= 4 and score_diff <= -9:
            return "QUESTIONABLE"
        elif wpa < -3:
            return "QUESTIONABLE"
    return "OK"

fourth_downs['GRADE'] = fourth_downs.apply(grade_decision, axis=1)
punts = fourth_downs[fourth_downs['PUNT_ATTEMPT'] == 1]

# ============================================
# HEADER
# ============================================
st.markdown('<p class="hero-title">SUPER BOWL LX</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">4th Down Decision Analysis</p>', unsafe_allow_html=True)

# Score display
st.markdown("""
<div class="score-display">
    <span class="team-sea">SEA 29</span>
    <span class="score-sep">—</span>
    <span class="team-ne">NE 13</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# KEY METRICS ROW
# ============================================
col1, col2, col3, col4 = st.columns(4)

bad_decisions = len(fourth_downs[fourth_downs['GRADE'].isin(['TERRIBLE', 'BAD'])])
questionable = len(fourth_downs[fourth_downs['GRADE'] == 'QUESTIONABLE'])
total_wpa = punts['WPA_PCT'].sum()
total_epa = punts['EPA'].sum()

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(punts)}</div>
        <div class="metric-label">4th Down Punts</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value bad">{bad_decisions}</div>
        <div class="metric-label">Bad Decisions</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value bad">{total_wpa:.1f}%</div>
        <div class="metric-label">WPA Lost</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value warn">{total_epa:.2f}</div>
        <div class="metric-label">EPA Lost</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# MAIN CONTENT: KEY PLAY + AI CHAT
# ============================================
play_col, chat_col = st.columns([1, 1], gap="large")

# KEY PLAY
with play_col:
    st.markdown('<div class="section-header">🔥 The Critical Moment</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="key-play-box">
        <div class="key-play-title">Q3 · 8:40 · Down 12-0</div>
        <div class="key-play-situation">4th & 1 at own 41</div>
        <div class="key-play-result">→ PUNTED</div>
    </div>
    """, unsafe_allow_html=True)
    
    key_play = fourth_downs[fourth_downs['YARDS_TO_GO'] == 1].iloc[0]
    
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Win Prob Before", f"{key_play['WIN_PROB_PCT']:.0f}%")
        st.metric("4th & 1 Conv Rate", "72%", help="NFL average conversion rate on 4th & 1")
    with m2:
        st.metric("WPA Impact", f"{key_play['WPA_PCT']:.1f}%", delta="Lost")
        st.metric("Decision", "PUNT 👎", delta="Wrong call")
    
    with st.expander("📊 The Math", expanded=False):
        st.markdown("""
        **Go for it scenario:**
        - 72% chance to convert → drive continues
        - 28% fail → SEA ball at NE 41
        
        **Punt scenario:**
        - SEA ball at ~SEA 15
        - Net gain: ~44 yards field position
        
        **Verdict:** Trading 72% conversion odds for 44 yards of field position while down 12 points is indefensible.
        """)

# AI CHAT
with chat_col:
    st.markdown('<div class="section-header">🤖 Ask the Analyst</div>', unsafe_allow_html=True)
    
    # Check connection status
    conn = get_snowflake_connection()
    if conn:
        st.markdown('<span class="status-dot connected"></span> <span style="color:#666;font-size:0.75rem;">Cortex Online</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-dot disconnected"></span> <span style="color:#666;font-size:0.75rem;">Offline</span>', unsafe_allow_html=True)
    
    # Initialize chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Chat history
    chat_container = st.container(height=300)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Quick prompts
    st.caption("Quick questions:")
    qcol1, qcol2 = st.columns(2)
    with qcol1:
        if st.button("Worst decision?", use_container_width=True):
            st.session_state.pending_question = "What was the worst 4th down decision and why?"
    with qcol2:
        if st.button("Go for it analysis", use_container_width=True):
            st.session_state.pending_question = "Should the Patriots have gone for it on 4th & 1?"
    
    # Chat input
    question = st.chat_input("Ask about the 4th down decisions...")
    
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
# DETAILED ANALYSIS TABS
# ============================================
tab1, tab2 = st.tabs(["📋 All Decisions", "📈 Win Probability"])

with tab1:
    st.markdown('<div class="section-header">Complete 4th Down Log</div>', unsafe_allow_html=True)
    
    display_df = fourth_downs.copy()
    display_df['QTR'] = 'Q' + display_df['QUARTER'].astype(str)
    display_df['SITUATION'] = '4th & ' + display_df['YARDS_TO_GO'].astype(str)
    display_df['SCORE'] = display_df['NE_SCORE'].astype(int).astype(str) + '-' + display_df['SEA_SCORE'].astype(int).astype(str)
    display_df['WP%'] = display_df['WIN_PROB_PCT'].apply(lambda x: f"{x:.0f}%")
    display_df['WPA'] = display_df['WPA_PCT'].apply(lambda x: f"{x:+.1f}%")
    
    # Add grade emoji
    def grade_emoji(g):
        if g == "TERRIBLE": return "🔴"
        if g == "BAD": return "🔴"
        if g == "QUESTIONABLE": return "🟡"
        return "✅"
    
    display_df[''] = display_df['GRADE'].apply(grade_emoji)
    
    show_cols = ['', 'QTR', 'TIME', 'SITUATION', 'FIELD_POSITION', 'SCORE', 'WP%', 'WPA', 'GRADE']
    
    st.dataframe(
        display_df[show_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "": st.column_config.TextColumn("", width="small"),
            "QTR": st.column_config.TextColumn("QTR", width="small"),
            "TIME": st.column_config.TextColumn("TIME", width="small"),
            "GRADE": st.column_config.TextColumn("GRADE", width="medium"),
        }
    )

with tab2:
    st.markdown('<div class="section-header">Win Probability Decline</div>', unsafe_allow_html=True)
    
    chart_df = fourth_downs.copy()
    chart_df['Play'] = range(1, len(chart_df) + 1)
    chart_df = chart_df.set_index('Play')
    
    st.line_chart(
        chart_df['WIN_PROB_PCT'],
        use_container_width=True,
        color="#ff4444"
    )
    
    st.caption("Each punt chipped away at New England's chances. The conservative approach guaranteed defeat.")
    
    # Summary stats
    scol1, scol2, scol3 = st.columns(3)
    with scol1:
        st.metric("Starting WP", "38%")
    with scol2:
        st.metric("Final WP", "6%")
    with scol3:
        st.metric("WP Lost to Punts", f"{abs(total_wpa):.1f}%")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p>Data: nflfastR · AI: Snowflake Cortex · Built with Streamlit</p>
    <p style="margin-top:0.5rem;">February 8, 2026 · Levi's Stadium · Santa Clara, CA</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### 📊 Legend")
    st.markdown("""
    **Metrics**
    - **WP** — Win Probability
    - **WPA** — Win Prob Added
    - **EPA** — Expected Points Added
    
    **Grades**
    - 🔴 **TERRIBLE/BAD** — Clear mistake
    - 🟡 **QUESTIONABLE** — Debatable
    - ✅ **OK** — Reasonable
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Connection")
    if get_snowflake_connection():
        st.success("Snowflake ✓")
    else:
        st.error("Disconnected")
