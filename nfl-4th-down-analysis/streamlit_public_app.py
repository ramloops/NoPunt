"""
Super Bowl LX 4th Down Analysis with Cortex AI
==============================================

Deploy to Snowflake Streamlit:
1. Go to Snowsight → Streamlit → + Streamlit App
2. Paste this code
3. Select your warehouse and NFL_DATA database

Features:
- Interactive 4th down analysis dashboard
- Cortex AI chatbot to ask questions about the data
- Win probability visualizations
"""

import streamlit as st
from snowflake.snowpark.context import get_active_session
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
# GET SNOWFLAKE SESSION
# ============================================
session = get_active_session()

# ============================================
# HEADER
# ============================================
st.title("🏈 Super Bowl LX: 4th Down Decision Analysis")
st.markdown("**Seahawks 29 - Patriots 13** | Powered by Cortex AI")

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_fourth_down_data():
    """Load Patriots 4th down decisions from Super Bowl LX"""
    query = """
    SELECT 
        PLAY_ID,
        QTR AS QUARTER,
        TIME,
        GAME_SECONDS_REMAINING,
        DOWN,
        YDSTOGO AS YARDS_TO_GO,
        YARDLINE_100,
        CASE 
            WHEN YARDLINE_100 > 50 THEN 'OWN ' || (100 - YARDLINE_100)
            WHEN YARDLINE_100 = 50 THEN 'MIDFIELD'
            ELSE 'OPP ' || YARDLINE_100
        END AS FIELD_POSITION,
        POSTEAM_SCORE AS NE_SCORE,
        DEFTEAM_SCORE AS SEA_SCORE,
        SCORE_DIFFERENTIAL,
        PLAY_TYPE,
        DESC AS PLAY_DESCRIPTION,
        YARDS_GAINED,
        ROUND(WP * 100, 1) AS WIN_PROB_PCT,
        ROUND(WPA * 100, 2) AS WPA_PCT,
        ROUND(EP, 2) AS EXPECTED_POINTS,
        ROUND(EPA, 2) AS EPA,
        FOURTH_DOWN_CONVERTED,
        FOURTH_DOWN_FAILED,
        PUNT_ATTEMPT,
        FIELD_GOAL_ATTEMPT
    FROM PLAY_BY_PLAY_2025
    WHERE POSTEAM = 'NE'
      AND DOWN = 4
      AND (HOME_TEAM = 'NE' AND AWAY_TEAM = 'SEA')
    ORDER BY GAME_SECONDS_REMAINING DESC
    """
    return session.sql(query).to_pandas()

@st.cache_data
def load_all_plays():
    """Load all Super Bowl plays for context"""
    query = """
    SELECT 
        QTR, TIME, POSTEAM, DEFTEAM, DOWN, YDSTOGO, 
        PLAY_TYPE, DESC, YARDS_GAINED,
        POSTEAM_SCORE, DEFTEAM_SCORE,
        ROUND(WP * 100, 1) AS WIN_PROB_PCT,
        ROUND(EPA, 2) AS EPA
    FROM PLAY_BY_PLAY_2025
    WHERE (HOME_TEAM = 'NE' AND AWAY_TEAM = 'SEA')
      AND PLAY_TYPE IS NOT NULL
    ORDER BY GAME_SECONDS_REMAINING DESC
    """
    return session.sql(query).to_pandas()

# Load data
try:
    fourth_downs = load_fourth_down_data()
    all_plays = load_all_plays()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

# ============================================
# TABS
# ============================================
tab1, tab2, tab3 = st.tabs(["📊 4th Down Analysis", "🔥 The Key Play", "🤖 Ask Cortex AI"])

# ============================================
# TAB 1: 4TH DOWN ANALYSIS
# ============================================
with tab1:
    if data_loaded and len(fourth_downs) > 0:
        st.header("Patriots 4th Down Decisions")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        punts = fourth_downs[fourth_downs['PUNT_ATTEMPT'] == 1]
        
        with col1:
            st.metric("Total 4th Downs", len(fourth_downs))
        with col2:
            st.metric("Punts", len(punts))
        with col3:
            total_wpa = punts['WPA_PCT'].sum() if 'WPA_PCT' in punts.columns else 0
            st.metric("Total WPA (Punts)", f"{total_wpa:.1f}%")
        with col4:
            total_epa = punts['EPA'].sum() if 'EPA' in punts.columns else 0
            st.metric("Total EPA (Punts)", f"{total_epa:.2f}")
        
        st.markdown("---")
        
        # Add decision grade
        def grade_decision(row):
            if row['PUNT_ATTEMPT'] == 1:
                if row['YARDS_TO_GO'] <= 1 and row['SCORE_DIFFERENTIAL'] <= -10:
                    return "🔴 TERRIBLE"
                elif row['YARDS_TO_GO'] <= 2 and row['SCORE_DIFFERENTIAL'] <= -7:
                    return "🔴 BAD"
                elif row['WPA_PCT'] < -2:
                    return "🟡 QUESTIONABLE"
            return "✅ OK"
        
        fourth_downs['GRADE'] = fourth_downs.apply(grade_decision, axis=1)
        
        # Display table
        display_cols = ['QUARTER', 'TIME', 'YARDS_TO_GO', 'FIELD_POSITION', 
                       'NE_SCORE', 'SEA_SCORE', 'PLAY_TYPE', 'WIN_PROB_PCT', 
                       'WPA_PCT', 'EPA', 'GRADE']
        
        available_cols = [c for c in display_cols if c in fourth_downs.columns]
        
        st.dataframe(
            fourth_downs[available_cols],
            use_container_width=True,
            hide_index=True
        )
        
        # Win Probability Chart
        st.subheader("Win Probability on 4th Downs")
        if 'WIN_PROB_PCT' in fourth_downs.columns:
            chart_data = fourth_downs[['QUARTER', 'TIME', 'WIN_PROB_PCT', 'PLAY_TYPE']].copy()
            chart_data['SITUATION'] = 'Q' + chart_data['QUARTER'].astype(str) + ' ' + chart_data['TIME'].astype(str)
            st.bar_chart(chart_data.set_index('SITUATION')['WIN_PROB_PCT'])
    else:
        st.warning("No 4th down data found. Make sure the data is loaded correctly.")

# ============================================
# TAB 2: THE KEY PLAY
# ============================================
with tab2:
    st.header("🔥 THE KEY PLAY: 4th & 1 from the 41")
    
    if data_loaded and len(fourth_downs) > 0:
        # Find the key play (4th & 1 or shortest yardage while losing big)
        key_plays = fourth_downs[
            (fourth_downs['YARDS_TO_GO'] <= 2) & 
            (fourth_downs['SCORE_DIFFERENTIAL'] < -7) &
            (fourth_downs['PUNT_ATTEMPT'] == 1)
        ]
        
        if len(key_plays) > 0:
            key_play = key_plays.iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Situation", f"4th & {int(key_play['YARDS_TO_GO'])}")
                st.metric("Field Position", key_play['FIELD_POSITION'])
                
            with col2:
                st.metric("Score", f"NE {int(key_play['NE_SCORE'])} - SEA {int(key_play['SEA_SCORE'])}")
                st.metric("Quarter", f"Q{int(key_play['QUARTER'])}")
                
            with col3:
                st.metric("Win Probability", f"{key_play['WIN_PROB_PCT']:.1f}%")
                st.metric("Decision", "PUNT 👎")
            
            st.markdown("---")
            
            # The math
            st.subheader("Why This Was Wrong")
            
            conv_rate = 0.72  # NFL average for 4th & 1
            
            st.markdown(f"""
            **NFL 4th & 1 Conversion Rate:** {conv_rate:.0%}
            
            **The Math:**
            - Win Prob before punt: **{key_play['WIN_PROB_PCT']:.1f}%**
            - WPA from punting: **{key_play['WPA_PCT']:.2f}%** (negative = hurt their chances)
            - EPA from punting: **{key_play['EPA']:.2f}**
            
            **If they went for it:**
            - 72% chance to convert → keep drive alive, likely score
            - 28% chance to fail → Seahawks get ball at NE 41 (not much different than punt!)
            
            **The Verdict:** Down 12 points in the 3rd quarter, you MUST be aggressive. 
            This punt was playing not to lose instead of playing to win.
            """)
            
            st.error(f"**Play Description:** {key_play['PLAY_DESCRIPTION']}")
        else:
            st.info("Looking for short-yardage punts while trailing...")
            st.dataframe(fourth_downs[fourth_downs['PUNT_ATTEMPT'] == 1])
    else:
        st.warning("Data not loaded")

# ============================================
# TAB 3: CORTEX AI CHAT
# ============================================
with tab3:
    st.header("🤖 Ask Cortex AI About the Game")
    
    st.markdown("""
    Ask questions about the Super Bowl LX data in natural language!
    
    **Example questions:**
    - "How many times did the Patriots punt on 4th down?"
    - "What was the Patriots' win probability when they punted on 4th & 1?"
    - "Which 4th down decisions hurt the Patriots the most?"
    - "Summarize all the bad punt decisions"
    """)
    
    # Chat input
    user_question = st.text_input("Ask a question about the game:", 
                                   placeholder="e.g., What was the worst 4th down decision?")
    
    if user_question:
        with st.spinner("Cortex AI is analyzing..."):
            
            # Build context from the data
            if data_loaded and len(fourth_downs) > 0:
                data_context = fourth_downs.to_string()
            else:
                data_context = "No data available"
            
            # Create prompt for Cortex
            prompt = f"""You are an NFL analytics expert analyzing Super Bowl LX (Seahawks 29, Patriots 13).

Here is the Patriots' 4th down data from the game:

{data_context}

Key context:
- The Patriots punted 8 times in this game
- They lost 29-13 to the Seahawks
- NFL average 4th & 1 conversion rate is 72%
- NFL average 4th & 2 conversion rate is 60%
- Negative WPA means the decision hurt their win probability
- Negative EPA means the decision cost them expected points

User question: {user_question}

Provide a clear, data-driven answer. Reference specific plays and numbers from the data when possible."""

            # Call Cortex AI
            try:
                response = session.sql(f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        'claude-3-5-sonnet',
                        '{prompt.replace("'", "''")}'
                    ) as response
                """).collect()[0]['RESPONSE']
                
                st.markdown("### Answer")
                st.markdown(response)
                
            except Exception as e:
                # Fallback to different model or show error
                try:
                    response = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.COMPLETE(
                            'mistral-large',
                            '{prompt.replace("'", "''")}'
                        ) as response
                    """).collect()[0]['RESPONSE']
                    
                    st.markdown("### Answer")
                    st.markdown(response)
                    
                except Exception as e2:
                    st.error(f"Cortex AI error: {e2}")
                    st.info("Make sure Cortex AI is enabled for your account. Run: ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US';")

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.header("About")
    st.markdown("""
    This app analyzes the Patriots' 4th down decisions 
    in Super Bowl LX using real play-by-play data from nflfastR.
    
    **Key Metrics:**
    - **WP** - Win Probability
    - **WPA** - Win Probability Added
    - **EP** - Expected Points
    - **EPA** - Expected Points Added
    
    **Data Source:** nflfastR / nflverse
    """)
    
    st.markdown("---")
    st.header("Quick Stats")
    
    if data_loaded and len(fourth_downs) > 0:
        st.metric("Total Plays (SB)", len(all_plays) if 'all_plays' in dir() else "N/A")
        st.metric("Patriots 4th Downs", len(fourth_downs))
        punts = len(fourth_downs[fourth_downs['PUNT_ATTEMPT'] == 1])
        st.metric("Punts", punts)
    
    st.markdown("---")
    st.caption("Built with Snowflake Streamlit + Cortex AI")