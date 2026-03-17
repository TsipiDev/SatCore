import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @keyframes glow {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    @keyframes slow-flash {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.2; }
    }
    @keyframes fast-flash {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    .nominal { animation: glow 2s infinite; color: #00FFB2; font-weight: bold; }
    .warning { animation: slow-flash 1.2s infinite; color: #FFD700; font-weight: bold; }
    .critical { animation: fast-flash 0.4s infinite; color: #FF4444; font-weight: bold; }
    .metric-nominal { animation: glow 2s infinite; color: #00FFB2; font-size: 1rem; }
    .metric-warning { animation: slow-flash 1.2s infinite; color: #FFD700; font-size: 1rem; }
    .metric-critical { animation: fast-flash 0.4s infinite; color: #FF4444; font-size: 1rem; }
    .info-nominal { animation: glow 2s infinite; color: #00FFB2; font-weight: bold; }
    .info-warning { animation: glow 2s infinite; color: #FFD700; font-weight: bold; }
    .info-critical { animation: glow 2s infinite; color: #FF4444; font-weight: bold; }
    .unknown { color: #FFFFFF; font-weight: bold; }
    .metric-unknown { color: #FFFFFF; font-size: 1rem; }
    .info-unknown { color: #FFFFFF; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)