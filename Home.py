import streamlit as st
from utils.styles import load_css
from utils.styles import load_sidebar

load_css()
load_sidebar("")

st.markdown("""
<style>
.block-container {
    padding-top: 1rem !important;
}
.satcore-header {
    text-align: center;
    padding: 0rem 0 1rem 0;
}
.satcore-title {
    font-size: 5rem !important;
    font-weight: 800;
    color: #00FFB2;
    letter-spacing: 0.5rem;
    margin-bottom: 0.2rem;
}
.satcore-subtitle {
    font-size: 0.85rem;
    color: #666666;
    letter-spacing: 0.3rem;
    margin-top: 0;
}
.satcore-divider {
    border: 1px solid #00FFB2;
    margin: 2rem 0;
    opacity: 0.2;
}
.module-card {
    border: 1px solid #1e2a3a;
    border-radius: 4px;
    padding: 1.2rem;
    margin-bottom: 0.5rem;
    background-color: #161C27;
}
.module-title {
    color: #00FFB2;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.1rem;
}
.module-desc {
    color: #888888;
    font-size: 0.85rem;
    margin-top: 0.3rem;
}
.status-bar {
    text-align: center;
    font-size: 0.75rem;
    color: #444;
    letter-spacing: 0.15rem;
    margin-top: 2rem;
}
.footer {
    text-align: center;
    margin-top: 1rem;
    padding-bottom: 2rem;
}
.footer p {
    font-size: 0.75rem;
    color: #444;
    letter-spacing: 0.1rem;
    margin-bottom: 0.5rem;
}
.footer a {
    color: #00FFB2;
    text-decoration: none;
    margin: 0 0.8rem;
    font-size: 1.5rem;
}
.footer a:hover {
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
""", unsafe_allow_html=True)

st.markdown("""
<div class="satcore-header">
    <p class="satcore-title">SATCORE</p>
    <p class="satcore-subtitle">SATELLITE MISSION CONTROL & TELEMETRY ANALYSIS PLATFORM</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="satcore-divider">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="module-card">
        <p class="module-title">HEALTH DASHBOARD</p>
        <p class="module-desc">Real-time spacecraft subsystem monitoring with status indicators and anomaly detection.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="module-card">
        <p class="module-title">TELEMETRY ANALYZER</p>
        <p class="module-desc">Historical telemetry analysis, anomaly event breakdown and threshold forecasting.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="module-card">
        <p class="module-title">PASS SCHEDULER</p>
        <p class="module-desc">Ground station pass predictions using real TLE orbital data from 14,000+ satellites.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="module-card">
        <p class="module-title">ORBIT VISUALIZER</p>
        <p class="module-desc">Real-time 3D orbital track visualization with live satellite position tracking.</p>
    </div>
    """, unsafe_allow_html=True)

col3, col4, col5 = st.columns([1, 2, 1])
with col4:
    st.markdown("""
    <div class="module-card">
        <p class="module-title">DATA IMPORT</p>
        <p class="module-desc">Import and map any decoded telemetry CSV to SatCore parameters.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="satcore-divider">', unsafe_allow_html=True)
st.markdown('<p class="status-bar">OPEN SOURCE &nbsp;|&nbsp; PYTHON &nbsp;|&nbsp; REAL ORBITAL DATA &nbsp;|&nbsp; LEO SATELLITE OPERATIONS</p>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <p>Developed by Dimitris Vatousis</p>
    <a href="https://github.com/TsipiDev" target="_blank"><i class="fab fa-github"></i></a>
    <a href="https://www.linkedin.com/in/dimitris-vatousis/" target="_blank"><i class="fab fa-linkedin"></i></a>
    <a href="https://tsipidev.github.io" target="_blank"><i class="fas fa-globe"></i></a>
</div>
""", unsafe_allow_html=True)