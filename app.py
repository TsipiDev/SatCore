import streamlit as st
from modules import health_dashboard
from modules import telemetry_analyzer
from modules import pass_scheduler


st.title("SatCore")

page = st.sidebar.radio("Navigation", ["Health Dashboard", "Telemetry Analyzer", "Pass Scheduler"])

if page == "Health Dashboard":
    health_dashboard.render()
elif page == "Telemetry Analyzer":
    telemetry_analyzer.render()
elif page == "Pass Scheduler":
    pass_scheduler.render()