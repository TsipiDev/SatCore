import streamlit as st
from modules import health_dashboard
from modules import telemetry_analyzer
from modules import pass_scheduler


st.title("SatCore")

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
</style>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["Health Dashboard", "Telemetry Analyzer", "Pass Scheduler"])

if page == "Health Dashboard":
    health_dashboard.render()
elif page == "Telemetry Analyzer":
    telemetry_analyzer.render()
elif page == "Pass Scheduler":
    pass_scheduler.render()