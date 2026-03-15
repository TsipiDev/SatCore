import streamlit as st
from modules import health_dashboard
from modules import telemetry_analyzer

st.title("SatCore")

page = st.sidebar.radio("Navigation", ["Health Dashboard", "Telemetry Analyzer"])

if page == "Health Dashboard":
    health_dashboard.render()
elif page == "Telemetry Analyzer":
    telemetry_analyzer.render()