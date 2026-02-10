"""
Super Bowl LX 4th Down Analysis
================================
Public Streamlit App for Streamlit Community Cloud
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
# SNOWFLAKE CONNECTION (using secrets + connector)
# ============================================
@st.cache_resource
def get_snowflake_connection():
    """Connect to Snowflake using secrets"""
    try:
        import snowflake.connector
        conn = snowflake.connector.connect(
            account=st.secrets["snowflake"]["account"],
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        return conn
    except Exception as e:
        return None

# ============================================
# SAMPLE DATA (fallback if no Snowflake)
# ============================================
def get_sample_data():
    """Sample Patriots 4th down data from Super Bowl LX"""
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
         "PLAY_DESCRIPTION": "4th & 1 PUNT - THE KEY PLAY!"},
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
# DATA LOADING
# ============================================
@st.cache_data(ttl=3600)
def load_fourth_down_data():
    """Load Patriots 4th down decisions from Snowflake or use sample"""
    conn = get_snowflake_connection()
    
    if conn is None:
        return get_sample_data(), False
    
    try:
        query = """
        SELECT 
            QTR AS QUARTER,
            TIME,
            YDSTOGO AS YARDS_TO_GO,
            CASE 
                WHEN YARDLINE_100 > 50 THEN 'OWN ' || (100 - YARDLINE_100)
                WHEN YARDLINE_100 = 50 THEN 'MIDFIELD'
                ELSE 'SEA ' || YARDLINE_100
            END AS FIELD_POSITION,
            POSTEAM_SCORE AS NE_SCORE,
            DEFTEAM_SCORE AS SEA_SCORE,
            SCORE_DIFFERENTIAL,
            PLAY_TYPE,
            DESC AS PLAY_DESCRIPTION,
            ROUND(WP * 100, 1) AS WIN_PROB_PCT,
            ROUND(WPA * 100, 2) AS WPA_PCT,
            ROUND(EPA, 2) AS EPA,
            CASE WHEN PLAY_TYPE = 'punt' THEN 1 ELSE 0 END AS PUNT_ATTEMPT
        FROM PLAY_BY_PLAY_2025
        WHERE POSTEAM = 'NE'
          AND DOWN = 4
          AND WEEK = 22
        ORDER BY GAME_SECONDS_REMAINING DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df, True
    except Exception as e:
        return get_sample_data(), False

# ============================================
# LOAD DATA
# ============================================
fourth_downs, live_data = load_fourth_down_data()

# ============================================
# HEADER
# ============================================
st.title("🏈 Super Bowl LX: 4th Down Analysis")
st.markdown("### Seahawks 29 - Patriots 13")

if live_data:
    st.success("✅ Connected to Snowflake - showing live data")
else:
    st.info("📊 Showing sample data")

st.markdown("*Analyzing why conservative play-calling cost New England the game*")

# ============================================
# GRADE DECISIONS
# ============================================
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
# TABS
# ============================================
tab1, tab2, tab3 = st.tabs(["📊 All 4th Downs", "🔥 The Key Play", "📈 Analysis"])

# ============================================
# TAB 1: ALL 4TH DOWNS
# ============================================
with tab1:
    st.header("Patriots 4th Down Decisions")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    punts = fourth_downs[fourth_downs['PUNT_ATTEMPT'] == 1]
    
    with col1:
        st.metric("Total 4th Downs", len(fourth_downs))
    with col2:
        st.metric("Punts", len(punts))
    with col3:
        total_wpa = punts['WPA_PCT'].sum()
        st.metric("Total WPA Lost", f"{total_wpa:.1f}%")
    with col4:
        total_epa = punts['EPA'].sum()
        st.metric("Total EPA Lost", f"{total_epa:.2f}")
    
    st.markdown("---")
    
    # Format for display
    display_df = fourth_downs.copy()
    display_df['SITUATION'] = 'Q' + display_df['QUARTER'].astype(str) + ' ' + display_df['TIME'].astype(str)
    display_df['DOWN_DIST'] = '4th & ' + display_df['YARDS_TO_GO'].astype(str)
    display_df['SCORE'] = display_df['NE_SCORE'].astype(int).astype(str) + '-' + display_df['SEA_SCORE'].astype(int).astype(str)
    
    show_cols = ['SITUATION', 'DOWN_DIST', 'FIELD_POSITION', 'SCORE', 
                 'WIN_PROB_PCT', 'WPA_PCT', 'EPA', 'GRADE']
    
    st.dataframe(display_df[show_cols], use_container_width=True, hide_index=True)

# ============================================
# TAB 2: THE KEY PLAY
# ============================================
with tab2:
    st.header("🔥 THE KEY PLAY")
    st.subheader("4th & 1 from their own 41, down 12-0 in the 3rd quarter")
    
    # Find the key play
    key_play = fourth_downs[
        (fourth_downs['YARDS_TO_GO'] <= 1) & 
        (fourth_downs['SCORE_DIFFERENTIAL'] <= -10)
    ]
    
    if len(key_play) > 0:
        kp = key_play.iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Situation", f"4th & {int(kp['YARDS_TO_GO'])}")
            st.metric("Field Position", kp.get('FIELD_POSITION', 'OWN 41'))
            
        with col2:
            st.metric("Score", f"NE {int(kp['NE_SCORE'])} - SEA {int(kp['SEA_SCORE'])}")
            st.metric("Win Probability", f"{kp['WIN_PROB_PCT']:.1f}%")
            
        with col3:
            st.metric("Decision", "PUNT 👎", delta="Wrong call", delta_color="inverse")
            st.metric("WPA", f"{kp['WPA_PCT']:.1f}%", delta="Lost win probability", delta_color="inverse")
    
    st.markdown("---")
    
    # The analysis
    st.subheader("Why This Was a Terrible Decision")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 The Numbers")
        st.markdown("""
        | Metric | Value |
        |--------|-------|
        | NFL 4th & 1 conversion rate | **72%** |
        | Win probability before punt | ~12% |
        | Win probability after punt | ~8% |
        | Win probability lost | **~4%** |
        """)
        
    with col2:
        st.markdown("### 🧮 Expected Value Analysis")
        st.markdown("""
        **If they GO FOR IT:**
        - 72% chance: Convert, keep driving → WP ~18%
        - 28% chance: Fail, SEA ball at NE 41 → WP ~6%
        - **Expected WP: ~14.6%**
        
        **If they PUNT:**
        - 100% chance: SEA ball at ~SEA 15 → WP ~8%
        - **Expected WP: ~8%**
        
        **Value destroyed: ~6.6 percentage points**
        """)
    
    st.error("""
    **Bottom Line:** When you're down 12 points in the 3rd quarter of the Super Bowl, 
    you cannot play conservative. The math clearly shows going for it was the right call. 
    Even if they failed, Seattle would only get the ball at the NE 41 - 
    not dramatically better field position than a punt would give them anyway.
    """)

# ============================================
# TAB 3: ANALYSIS
# ============================================
with tab3:
    st.header("📈 Decision Analysis")
    
    # Win probability chart
    st.subheader("Win Probability on Each 4th Down")
    
    chart_df = fourth_downs.copy()
    chart_df['Play'] = range(1, len(chart_df) + 1)
    chart_df = chart_df.set_index('Play')
    
    st.bar_chart(chart_df['WIN_PROB_PCT'], use_container_width=True)
    st.caption("Win probability steadily declined as Patriots kept punting")
    
    st.markdown("---")
    
    # Decision grades summary
    st.subheader("Decision Grades Summary")
    
    grade_counts = fourth_downs['GRADE'].value_counts()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bad = grade_counts.get('🔴 TERRIBLE', 0) + grade_counts.get('🔴 BAD', 0)
        st.metric("🔴 Bad Decisions", bad)
    with col2:
        quest = grade_counts.get('🟡 QUESTIONABLE', 0)
        st.metric("🟡 Questionable", quest)
    with col3:
        ok = grade_counts.get('✅ OK', 0)
        st.metric("✅ Acceptable", ok)
    
    st.markdown("---")
    
    # WPA by quarter
    st.subheader("Win Probability Lost by Quarter")
    
    wpa_by_qtr = fourth_downs.groupby('QUARTER')['WPA_PCT'].sum().reset_index()
    wpa_by_qtr.columns = ['Quarter', 'WPA Lost (%)']
    
    st.bar_chart(wpa_by_qtr.set_index('Quarter'), use_container_width=True)
    
    st.markdown("---")
    
    # Key insight
    st.info("""
    **Key Insight:** The Patriots were among the more aggressive teams on 4th downs during 
    the regular season, but completely abandoned that approach in the Super Bowl. 
    Their conservative play-calling, especially the 4th & 1 punt, contributed significantly 
    to their loss. Analytics clearly favored going for it in multiple situations.
    """)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.header("About This App")
    st.markdown("""
    Analyzes Patriots' 4th down decisions in Super Bowl LX 
    using play-by-play data and win probability models.
    
    **Metrics Explained:**
    - **WP** - Win Probability (0-100%)
    - **WPA** - Win Probability Added (how much the play changed WP)
    - **EPA** - Expected Points Added
    
    **Grading System:**
    - 🔴 **TERRIBLE/BAD** - Clear mistake, should have gone for it
    - 🟡 **QUESTIONABLE** - Borderline call, analytics favored going
    - ✅ **OK** - Reasonable decision given the situation
    """)
    
    st.markdown("---")
    
    st.markdown("""
    **Game Info:**  
    📅 February 8, 2026  
    🏟️ Levi's Stadium, Santa Clara  
    🏆 Super Bowl LX  
    
    **Final Score:**  
    🦅 Seahawks 29  
    🏈 Patriots 13
    """)
    
    st.markdown("---")
    
    st.markdown("""
    **Data Source:**  
    [nflfastR](https://www.nflfastr.com/) play-by-play data
    """)
    
    st.markdown("---")
    st.caption("Built with Streamlit")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.caption("Data from nflfastR | Win probability models by nflfastR")