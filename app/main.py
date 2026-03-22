import sys
import os

sys.path.append(os.getcwd())

import streamlit as st
import pandas as pd
import plotly.express as px
from src.evaluation import get_performance_metrics

# ----------------------------
# 1. Professional Login System
# ----------------------------
def login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        # Load NPCI logo from assets
        if os.path.exists("assets/npci_logo.png"):
            st.image("assets/npci_logo.png", width=200)
        st.title("TECHKRITI'26 | NPCI Sentinel")
        st.subheader("Cyber-Security Hackathon Portal")
        
        user = st.text_input("Administrator ID")
        pw = st.text_input("Access Key", type="password")
        
        if st.button("Authenticate"):
            if user == "admin" and pw == "npci2026":  # Professional credentials
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

login()

# ----------------------------
# 2. Page Configuration
# ----------------------------
st.set_page_config(
    page_title="NPCI Sentinel | Enterprise Threat Intel",
    page_icon="assets/npci_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# 3. Tabs Styling (Professional)
# ----------------------------
st.markdown("""
    <style>
    /* Tabs container */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 28px; 
        border-bottom: 2px solid #0d7377;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab"] { 
        height: 48px; 
        white-space: pre; 
        background-color: #19232f; 
        border-radius: 6px 6px 0 0; 
        color: #e0e6e8;
        font-weight: 600;
        transition: background-color 0.3s ease;
        cursor: pointer;
        padding: 10px 20px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #0d7377;
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab"]:focus {
        outline: none;
        box-shadow: 0 0 5px #0d7377;
    }
    .stTabs [data-baseweb="tab--selected"] {
        background-color: #0d7377;
        color: #ffffff;
        font-weight: 700;
        box-shadow: inset 0 -2px 0 #00ffc3;
    }

    /* Fix content below tabs being cut */
    .stTabs > div[data-testid="stHorizontalBlock"] {
        padding-top: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 4. Load Data
# ----------------------------
@st.cache_data
def load_sentinel_data():
    try:
        data = pd.read_csv('data/final_results.csv')
        data['hour'] = data['hour'].astype(int)
        return data
    except FileNotFoundError:
        return None

df = load_sentinel_data()

# ----------------------------
# 5. Sidebar
# ----------------------------
with st.sidebar:
    # NPCI Logo at the top of sidebar
    if os.path.exists("assets/npci_logo.png"):
        st.image("assets/npci_logo.png", width=150)

    st.title("Sentinel SOC")
    st.status("Engine: Operational", state="complete")
    st.info("Privacy Active: SHA-256 Pseudonymization enabled for all PII fields.")
    
    st.divider()
    risk_threshold = st.slider("Detection Sensitivity (Threshold)", 0, 100, 80)
    st.caption("Adjusting this balances Precision vs. Recall in real-time.")

    # ----------------------------
    # Logout Button
    # ----------------------------
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun = None
        st.stop()
# ----------------------------
# 6. Main Dashboard
# ----------------------------
if df is not None:
    st.title("NPCI Sentinel: AI Insider Threat Platform")
    st.markdown("##### Hybrid Behavioral-Psychometric Detection Engine")
    
    # Tabs
    tab_dash, tab_perf = st.tabs(["Threat Command Center", "Performance Analytics"])

    with tab_dash:
        # Summary Statistics
        m1, m2, m3, m4 = st.columns(4)
        flagged_count = len(df[df['risk_score'] >= risk_threshold])
        
        m1.metric("Total Events Analyzed", f"{len(df):,}")
        m2.metric("Critical Red Flags", flagged_count, delta=f"{flagged_count} alerts", delta_color="inverse")
        m3.metric("Fleet Risk Index", f"{df['risk_score'].mean():.1f}%")
        m4.metric("Privacy Status", "AES-256 Hashed")

        st.divider()

        # High-Risk Queue
        col_table, col_dist = st.columns([3, 2])

        with col_table:
            st.subheader("High-Risk Activity Queue")
            alerts = df[df['risk_score'] >= risk_threshold].sort_values('risk_score', ascending=False)
            
            st.dataframe(
                alerts[['user_hash', 'risk_score', 'threat_reason', 'hour', 'is_night']],
                column_config={
                    "risk_score": st.column_config.ProgressColumn("Risk Index", min_value=0, max_value=100, format="%d%%"),
                    "threat_reason": "Explanation (SHAP)",
                    "user_hash": "Anonymized ID",
                    "is_night": "After Hours"
                },
                width="stretch", 
                hide_index=True
            )

        with col_dist:
            st.subheader("Risk Distribution")
            fig_hist = px.histogram(df, x="risk_score", nbins=50, color_discrete_sequence=['#30363d'])
            fig_hist.add_vline(x=risk_threshold, line_dash="dash", line_color="#ff4b4b", annotation_text="Active Threshold")
            fig_hist.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=20, b=0), height=320)
            st.plotly_chart(fig_hist, width="stretch")

        # Behavioral Trends
        st.divider()
        st.subheader("Organizational Risk Heatmap (24h Cycle)")
        hourly_risk = df.groupby('hour')['risk_score'].mean().reset_index()
        fig_area = px.area(hourly_risk, x='hour', y='risk_score', color_discrete_sequence=['#ff4b4b'])
        fig_area.update_layout(template="plotly_dark", height=300, xaxis=dict(dtick=2))
        st.plotly_chart(fig_area, width="stretch")

    with tab_perf:
        st.header("Model Evaluation & Precision Report")
        metrics = get_performance_metrics(df)
        
        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Precision", metrics["Precision"])
        p2.metric("Recall", metrics["Recall"])
        p3.metric("F1-Score", metrics["F1 Score"])
        p4.metric("Accuracy", metrics["Accuracy"])
        
        st.divider()
        st.subheader("Technical Architecture Summary")
        st.write("""
        - **Engine:** Two-Tier Ensemble (Isolation Forest + Deep Autoencoders)
        - **Explainability:** Integrated SHAP values for model transparency
        - **Scalability:** Modular Python backend capable of handling CMU-sized datasets
        - **Privacy:** Multi-stage hashing ensures zero exposure of PII
        """)

else:
    st.error("System Offline: Please run `python main_pipeline.py` to initialize the detection engine.")