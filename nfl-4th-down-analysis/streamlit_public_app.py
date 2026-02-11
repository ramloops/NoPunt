"""
Super Bowl LX 4th Down Analysis
================================
Original UX with Dark Mode
"""

import streamlit as st
import pandas as pd

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Super Bowl LX: 4th Down Analysis",
    page_icon="🏈",
    layout="wide"
)

# ============================================
# THEME TOGGLE
# ============================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark

# Toggle in sidebar
with st.sidebar:
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)

# Mobile-responsive base CSS (shared between themes)
mobile_css = """
    /* Hide Streamlit header, footer, and menu */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    
    /* Reduce top padding since header is hidden */
    .main .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 0.5rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        /* Stack columns vertically on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        
        /* Smaller title on mobile */
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2, h3 {
            font-size: 1.2rem !important;
        }
        
        /* Smaller metrics on mobile */
        [data-testid="stMetricValue"] {
            font-size: 1.25rem !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.75rem !important;
        }
        
        /* Better tab sizing on mobile */
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 0.75rem !important;
            font-size: 0.85rem !important;
        }
        
        /* Full width buttons on mobile */
        .stButton > button {
            width: 100% !important;
            padding: 0.5rem !important;
            font-size: 0.85rem !important;
        }
        
        /* Adjust chat input on mobile */
        [data-testid="stChatInput"] textarea {
            font-size: 16px !important; /* Prevents zoom on iOS */
        }
        
        /* Smaller text in chat */
        [data-testid="stChatMessage"] {
            font-size: 0.9rem !important;
        }
        
        /* Better dataframe on mobile */
        .stDataFrame {
            font-size: 0.75rem !important;
        }
        
        /* Reduce spacing */
        hr {
            margin-top: 1rem !important;
            margin-bottom: 1rem !important;
        }
    }
    
    /* Small phone adjustments */
    @media (max-width: 480px) {
        h1 {
            font-size: 1.25rem !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.4rem 0.5rem !important;
            font-size: 0.75rem !important;
        }
    }
"""

# Dark mode CSS
if st.session_state.dark_mode:
    st.markdown(f"""
    <style>
        {mobile_css}
        
        /* Dark background */
        .stApp {{
            background-color: #0e1117;
            color: #fafafa;
        }}
        
        /* Sidebar dark */
        [data-testid="stSidebar"] {{
            background-color: #161b22;
        }}
        
        /* Metric styling */
        [data-testid="stMetricValue"] {{
            color: #ffffff;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: #8b949e;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            color: #8b949e;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: #21262d;
            color: #ffffff;
        }}
        
        /* Dataframe */
        .stDataFrame {{
            background-color: #161b22;
        }}
        
        /* Chat messages */
        [data-testid="stChatMessage"] {{
            background-color: #161b22;
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: #21262d;
            color: #ffffff;
            border: 1px solid #30363d;
        }}
        
        .stButton > button:hover {{
            background-color: #30363d;
            border-color: #8b949e;
        }}
        
        /* Chat input */
        [data-testid="stChatInput"] {{
            background-color: #161b22;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: #161b22;
            color: #ffffff;
        }}
        
        /* Dividers */
        hr {{
            border-color: #30363d;
        }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <style>
        {mobile_css}
        
        /* Light background */
        .stApp {{
            background-color: #ffffff;
            color: #1a1a1a;
        }}
        
        /* Sidebar light */
        [data-testid="stSidebar"] {{
            background-color: #f6f8fa;
        }}
        
        /* Metric styling */
        [data-testid="stMetricValue"] {{
            color: #1a1a1a;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: #57606a;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            color: #57606a;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: #f6f8fa;
            color: #1a1a1a;
        }}
        
        /* Dataframe */
        .stDataFrame {{
            background-color: #f6f8fa;
        }}
        
        /* Chat messages */
        [data-testid="stChatMessage"] {{
            background-color: #f6f8fa;
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: #f6f8fa;
            color: #1a1a1a;
            border: 1px solid #d0d7de;
        }}
        
        .stButton > button:hover {{
            background-color: #eaeef2;
            border-color: #57606a;
        }}
        
        /* Chat input */
        [data-testid="stChatInput"] {{
            background-color: #f6f8fa;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: #f6f8fa;
            color: #1a1a1a;
        }}
        
        /* Dividers */
        hr {{
            border-color: #d0d7de;
        }}
    </style>
    """, unsafe_allow_html=True)

# ============================================
# SNOWFLAKE CONNECTION
# ============================================
@st.cache_resource
def get_snowflake_connection():
    """Create Snowflake connection from secrets (supports password or key-pair auth)"""
    try:
        import snowflake.connector
        
        sf_config = st.secrets["snowflake"]
        
        # Base connection params
        conn_params = {
            "account": sf_config["account"],
            "user": sf_config["user"],
            "warehouse": sf_config["warehouse"],
            "database": sf_config["database"],
            "schema": sf_config["schema"],
        }
        
        # Check for key-pair auth (preferred) or password auth
        if "private_key" in sf_config:
            # Key-pair authentication
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives import serialization
            
            private_key_text = sf_config["private_key"]
            
            # Load the private key
            p_key = serialization.load_pem_private_key(
                private_key_text.encode(),
                password=None,
                backend=default_backend()
            )
            
            # Get the raw bytes for Snowflake
            pkb = p_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            conn_params["private_key"] = pkb
        elif "password" in sf_config:
            # Password authentication (may not work with MFA)
            conn_params["password"] = sf_config["password"]
        else:
            st.error("No authentication method found in secrets (need 'password' or 'private_key')")
            return None
        
        conn = snowflake.connector.connect(**conn_params)
        return conn
        
    except Exception as e:
        st.error(f"Snowflake connection error: {e}")
        return None

# ============================================
# SAMPLE DATA
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
# AI CHAT FUNCTION - SNOWFLAKE CORTEX
# ============================================
def get_ai_response(question, fourth_downs_df):
    """Get AI response using Snowflake Cortex via SQL"""
    
    # Build context from data
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

    # Combine system prompt and user question
    full_prompt = f"{system_prompt}\n\nUser question: {question}"
    
    # Try Snowflake Cortex first
    try:
        conn = get_snowflake_connection()
        if conn:
            cursor = conn.cursor()
            
            # Set role and warehouse
            cursor.execute("USE ROLE SYSADMIN")
            cursor.execute(f"USE WAREHOUSE {st.secrets['snowflake']['warehouse']}")
            
            # Escape single quotes in the prompt for SQL
            escaped_prompt = full_prompt.replace("'", "''")
            
            # Call Cortex COMPLETE function
            sql = f"""
            SELECT SNOWFLAKE.CORTEX.COMPLETE(
                'mistral-large',
                '{escaped_prompt}'
            ) as response
            """
            
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
            
            if result and result[0]:
                return result[0]
            else:
                return "No response from Cortex"
                
    except Exception as e:
        error_msg = str(e)
        
        # If Cortex fails, try Anthropic as fallback
        if "ANTHROPIC_API_KEY" in st.secrets:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=500,
                    system=system_prompt,
                    messages=[{"role": "user", "content": question}]
                )
                return message.content[0].text
            except Exception as anthropic_error:
                return f"Cortex error: {error_msg[:100]}\n\nAnthropic fallback error: {str(anthropic_error)[:100]}"
        
        return f"Cortex error: {error_msg[:200]}"

# ============================================
# LOAD DATA
# ============================================
fourth_downs = get_fourth_down_data()

# Grade decisions
def grade_decision(row):
    ydstogo = row.get('YARDS_TO_GO', 10)
    score_diff = row.get('SCORE_DIFFERENTIAL', 0)
    wpa = row.get('WPA_PCT', 0)
    punt = row.get('PUNT_ATTEMPT', 0)
    
    if punt == 1:
        if ydstogo <= 1 and score_diff <= -10:
            return "🔴 TERRIBLE"
        elif ydstogo <= 2 and score_diff <= -7:
            return "🔴 BAD"
        elif ydstogo <= 4 and score_diff <= -9:
            return "🟡 QUESTIONABLE"
        elif wpa < -3:
            return "🟡 QUESTIONABLE"
    return "✅ OK"

fourth_downs['GRADE'] = fourth_downs.apply(grade_decision, axis=1)

# ============================================
# HEADER
# ============================================
st.title("🏈 Super Bowl LX: 4th Down Analysis")
st.markdown("### Seahawks 29 - Patriots 13")
st.markdown("*Why conservative play-calling cost New England the game*")

# ============================================
# HOME SCREEN: AI CHAT + KEY STATS
# ============================================

# Top row: Key metrics
col1, col2, col3, col4 = st.columns(4)

punts = fourth_downs[fourth_downs['PUNT_ATTEMPT'] == 1]

with col1:
    st.metric("4th Down Punts", len(punts))
with col2:
    bad_decisions = len(fourth_downs[fourth_downs['GRADE'].str.contains('🔴|🟡')])
    st.metric("Bad/Questionable", bad_decisions)
with col3:
    total_wpa = punts['WPA_PCT'].sum()
    st.metric("Total WPA Lost", f"{total_wpa:.1f}%")
with col4:
    total_epa = punts['EPA'].sum()
    st.metric("Total EPA Lost", f"{total_epa:.2f}")

st.markdown("---")

# ============================================
# TABS: All content in tabs to avoid scrolling
# ============================================
tab_home, tab_data, tab_analysis = st.tabs(["🏠 Overview", "📊 All 4th Downs", "📈 Analysis"])

with tab_home:
    # Two columns: AI Chat on left, Key Play on right
    chat_col, play_col = st.columns([1, 1])

    # ============================================
    # LEFT: AI CHAT
    # ============================================
    with chat_col:
        st.subheader("🤖 Ask About the Game")
        st.caption("Powered by Snowflake Cortex")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Example questions
        st.caption("Try asking:")
        example_cols = st.columns(2)
        with example_cols[0]:
            if st.button("What was the worst decision?", use_container_width=True):
                st.session_state.pending_question = "What was the worst 4th down decision and why?"
        with example_cols[1]:
            if st.button("Should they have gone for it?", use_container_width=True):
                st.session_state.pending_question = "Should the Patriots have gone for it on 4th & 1?"
        
        # Chat input
        question = st.chat_input("Ask about Patriots' 4th down decisions...")
        
        # Handle pending question from button click
        if "pending_question" in st.session_state:
            question = st.session_state.pending_question
            del st.session_state.pending_question
        
        if question:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing with Cortex..."):
                    response = get_ai_response(question, fourth_downs)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    # ============================================
    # RIGHT: THE KEY PLAY
    # ============================================
    with play_col:
        st.subheader("🔥 The Key Play")
        
        # Highlight box
        st.error("**4th & 1 from own 41, down 12-0 in Q3 → PUNT**")
        
        key_play = fourth_downs[fourth_downs['YARDS_TO_GO'] == 1].iloc[0]
        
        kp_col1, kp_col2 = st.columns(2)
        with kp_col1:
            st.metric("Win Prob Before", f"{key_play['WIN_PROB_PCT']:.1f}%")
            st.metric("NFL 4th & 1 Conv Rate", "72%")
        with kp_col2:
            st.metric("WPA from Punt", f"{key_play['WPA_PCT']:.1f}%", delta="Lost", delta_color="inverse")
            st.metric("Decision", "PUNT 👎")
        
        st.markdown("""
        **The Math:**
        - Go for it: 72% convert → keep drive alive
        - Even if fail: SEA gets ball at NE 41
        - Punt: SEA gets ball at ~SEA 15
        
        **Net field position gain from punt: ~44 yards**  
        **Not worth giving up 72% chance to convert!**
        """)

with tab_data:
    st.header("All Patriots 4th Down Decisions")
    
    display_df = fourth_downs.copy()
    display_df['SITUATION'] = 'Q' + display_df['QUARTER'].astype(str) + ' ' + display_df['TIME'].astype(str)
    display_df['DOWN_DIST'] = '4th & ' + display_df['YARDS_TO_GO'].astype(str)
    display_df['SCORE'] = display_df['NE_SCORE'].astype(int).astype(str) + '-' + display_df['SEA_SCORE'].astype(int).astype(str)
    
    show_cols = ['SITUATION', 'DOWN_DIST', 'FIELD_POSITION', 'SCORE', 
                 'WIN_PROB_PCT', 'WPA_PCT', 'EPA', 'GRADE']
    
    st.dataframe(display_df[show_cols], use_container_width=True, hide_index=True)

with tab_analysis:
    st.header("Decision Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Win Probability Trend")
        chart_df = fourth_downs.copy()
        chart_df['Play #'] = range(1, len(chart_df) + 1)
        st.bar_chart(chart_df.set_index('Play #')['WIN_PROB_PCT'])
        st.caption("Win probability dropped with each conservative punt")
    
    with col2:
        st.subheader("Decision Grades")
        grade_counts = fourth_downs['GRADE'].value_counts()
        
        gcol1, gcol2, gcol3 = st.columns(3)
        with gcol1:
            bad = grade_counts.get('🔴 TERRIBLE', 0) + grade_counts.get('🔴 BAD', 0)
            st.metric("🔴 Bad", bad)
        with gcol2:
            st.metric("🟡 Questionable", grade_counts.get('🟡 QUESTIONABLE', 0))
        with gcol3:
            st.metric("✅ OK", grade_counts.get('✅ OK', 0))

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.header("Super Bowl LX")
    st.markdown("""
    🦅 **Seahawks 29**  
    🏈 **Patriots 13**
    
    📅 February 8, 2026  
    🏟️ Levi's Stadium
    """)
    
    st.markdown("---")
    
    st.markdown("""
    **Metrics:**
    - **WP** - Win Probability
    - **WPA** - Win Prob Added
    - **EPA** - Expected Points Added
    
    **Grades:**
    - 🔴 Should have gone for it
    - 🟡 Borderline / questionable
    - ✅ Reasonable decision
    """)
    
    st.markdown("---")
    
    # Connection status
    st.subheader("🔌 Status")
    try:
        conn = get_snowflake_connection()
        if conn:
            st.success("Snowflake: Connected")
        else:
            st.error("Snowflake: Not connected")
    except:
        st.error("Snowflake: Error")
    
    st.markdown("---")
    st.caption("Data: nflfastR | AI: Snowflake Cortex")

st.markdown("---")
st.caption("Built with Streamlit + Snowflake Cortex")
