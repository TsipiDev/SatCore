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
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.8); }
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
    .panel {
        border: 1px solid #1e2a3a;
        border-radius: 4px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        background-color: #161C27;
    }
    .panel-title {
    font-size: 0.7rem;
    color: #FFFFFF;
    letter-spacing: 0.2rem;
    margin-bottom: 1rem;
    text-transform: uppercase;
    opacity: 0.7;
    }
    .page-title {
    font-size: 3rem !important;
    font-weight: 700;
    color: #00FFB2;
    letter-spacing: 0.15rem;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
    padding-top: 1rem;
    }
    .page-subtitle {
        font-size: 0.7rem;
        color: #444;
        letter-spacing: 0.2rem;
        margin-bottom: 1.5rem;
    }
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)


def load_sidebar(current_page):
    st.sidebar.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 0 1.5rem 0;
        border-bottom: 1px solid #1e2a3a;
        margin-bottom: 1rem;
    }
    .sidebar-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #00FFB2;
        letter-spacing: 0.4rem;
        margin-bottom: 0;
    }
    .sidebar-subtitle {
        font-size: 0.55rem;
        color: #444;
        letter-spacing: 0.2rem;
        margin-top: 0.2rem;
    }
    .sidebar-status {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        margin-top: 0.8rem;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #00FFB2;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    .status-text {
        font-size: 0.6rem;
        color: #00FFB2;
        letter-spacing: 0.15rem;
    }
    .sidebar-version {
        font-size: 0.55rem;
        color: #333;
        letter-spacing: 0.1rem;
        text-align: center;
        margin-top: 0.4rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div class="sidebar-header">
        <p class="sidebar-title">SATCORE</p>
        <p class="sidebar-subtitle">SATELLITE MISSION CONTROL</p>
        <div class="sidebar-status">
            <span class="status-dot"></span>
            <span class="status-text">SYSTEM ONLINE</span>
        </div>
        <p class="sidebar-version">v1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

    pages = [
        ("", "Home", '<i class="fas fa-house"></i>'),
        ("Data_Import", "Data Import", '<i class="fas fa-file-import"></i>'),
        ("Health_Dashboard", "Health Dashboard", '<i class="fas fa-satellite"></i>'),
        ("Telemetry_Analyzer", "Telemetry Analyzer", '<i class="fas fa-chart-line"></i>'),
        ("Pass_Scheduler", "Pass Scheduler", '<i class="fas fa-satellite-dish"></i>'),
        ("Orbit_Visualizer", "Orbit Visualizer", '<i class="fas fa-globe"></i>'),
    ]

    for page_id, page_name, icon in pages:
        is_active = current_page == page_id
        color = "#00FFB2" if is_active else "#888888"
        weight = "700" if is_active else "400"
        bg = "background-color: #161C27; border-left: 2px solid #00FFB2;" if is_active else ""
        st.sidebar.markdown(f"""
        <a href="/{page_id}" target="_self" style="text-decoration: none;">
            <div style="padding: 0.6rem 1rem; margin: 0.2rem 0; border-radius: 4px; {bg} cursor: pointer;">
                <span style="color: {color}; font-size: 0.9rem; font-weight: {weight}; letter-spacing: 0.05rem;">
                    {icon} &nbsp; {page_name}
                </span>
            </div>
        </a>
        """, unsafe_allow_html=True)