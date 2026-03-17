import streamlit as st
import pandas as pd
import plotly.express as px


def get_status(value, warn_low, crit_low, warn_high=None, crit_high=None):
    try:
        value = float(value)
    except:
        return "unknown", "NOT PROVIDED"
    if value == 0:
        return "unknown", "NOT PROVIDED"
    if value <= crit_low:
        return "critical", "CRITICAL"
    elif crit_high and value >= crit_high:
        return "critical", "CRITICAL"
    elif value <= warn_low:
        return "warning", "WARNING"
    elif warn_high and value >= warn_high:
        return "warning", "WARNING"
    return "nominal", "NOMINAL"


def fmt(value, decimals=2, unit=""):
    try:
        v = float(value)
        if v == 0:
            return "N/A"
        return f"{v:.{decimals}f} {unit}".strip()
    except:
        return "N/A"


def render():

    st.markdown('<p class="page-title">Health Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">REAL-TIME SPACECRAFT SUBSYSTEM MONITORING</p>', unsafe_allow_html=True)

    df = pd.read_csv("data/telemetry/sample_telemetry.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.sort_values("timestamp", ascending=False)

    if df["eps_solar_current_ma"].dtype != object:
        df["eps_solar_current_a"] = df["eps_solar_current_ma"] / 1000
    else:
        df["eps_solar_current_a"] = 0

    df_plot = df.sort_values("timestamp").set_index("timestamp").resample("1h").mean(numeric_only=True).reset_index()

    latest = df.iloc[0]

    batt_v_class, _ = get_status(latest["eps_batt_voltage_v"], 7.2, 6.8)
    batt_t_class, _ = get_status(latest["eps_batt_temp_c"], 0, -5, 30, 40)
    solar_v_class, _ = get_status(latest["eps_solar_voltage_v"], 4.5, 4.0)
    solar_i_class, _ = get_status(latest["eps_solar_current_ma"], 1200, 900)
    obc_temp_class, _ = get_status(latest["obc_temp_c"], 0, -5, 40, 50)
    adcs_class, _ = get_status(latest["adcs_attitude_error_deg"], -1, -1, 0.3, 0.7)
    rssi_class, _ = get_status(latest["comms_rssi_dbm"], -90, -100)

    mode_val = str(latest["mode"])
    adcs_val = str(latest["adcs_mode"])
    mode_class = "unknown" if mode_val == "Not Provided" else ("nominal" if mode_val == "NOMINAL" else "warning" if mode_val == "WARNING" else "critical")
    adcs_mode_class = "unknown" if adcs_val == "Not Provided" else ("nominal" if adcs_val == "NOMINAL" else "warning")

    st.markdown('<div class="panel"><p class="panel-title">SPACECRAFT STATUS</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<p>Mission Mode<br><span class="{mode_class}" style="font-size:1.8rem;">{mode_val}</span></p>', unsafe_allow_html=True)
    c2.markdown(f'<p>ADCS Mode<br><span class="{adcs_mode_class}" style="font-size:1.8rem;">{adcs_val}</span></p>', unsafe_allow_html=True)
    c3.metric("Uptime", fmt(latest["obc_uptime_s"], 0, "s"))
    st.markdown(f"""
    <p>Power: <span class="{batt_v_class}">{batt_v_class.upper()}</span> &nbsp;&nbsp;|&nbsp;&nbsp; Thermal: <span class="{obc_temp_class}">{obc_temp_class.upper()}</span></p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><p class="panel-title">POWER</p>', unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    p1.markdown(f'<p class="metric-{batt_v_class}">Batt Voltage<br><span style="font-size:1.8rem; font-weight:600;">{fmt(latest["eps_batt_voltage_v"], 2, "V")}</span></p>', unsafe_allow_html=True)
    p2.markdown(f'<p class="metric-{batt_t_class}">Batt Temp<br><span style="font-size:1.8rem; font-weight:600;">{fmt(latest["eps_batt_temp_c"], 1, "C")}</span></p>', unsafe_allow_html=True)
    p3.markdown(f'<p class="metric-{solar_v_class}">Solar Voltage<br><span style="font-size:1.8rem; font-weight:600;">{fmt(latest["eps_solar_voltage_v"], 2, "V")}</span></p>', unsafe_allow_html=True)
    p4.markdown(f'<p class="metric-{solar_i_class}">Solar Current<br><span style="font-size:1.8rem; font-weight:600;">{fmt(latest["eps_solar_current_ma"], 0, "mA")}</span></p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><p class="panel-title">SYSTEMS</p>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    s1.markdown(f'<p class="metric-{obc_temp_class}">OBC Temp<br><span style="font-size:1.8rem; font-weight:600;">{fmt(latest["obc_temp_c"], 1, "C")}</span></p>', unsafe_allow_html=True)
    s2.markdown(f'<p class="metric-{adcs_class}">Attitude Error<br><span style="font-size:1.8rem; font-weight:600;">{fmt(latest["adcs_attitude_error_deg"], 2, "deg")}</span></p>', unsafe_allow_html=True)
    s3.markdown(f'<p class="metric-{rssi_class}">Signal (RSSI)<br><span style="font-size:1.8rem; font-weight:600;">{fmt(latest["comms_rssi_dbm"], 1, "dBm")}</span></p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><p class="panel-title">TELEMETRY CHARTS</p>', unsafe_allow_html=True)
    with st.expander("Power", expanded=True):
        st.markdown("<h4 style='text-align: center;'>Power</h4>", unsafe_allow_html=True)
        power_fig = px.line(df_plot, x="timestamp", y=["eps_batt_voltage_v", "eps_solar_current_a"])
        st.plotly_chart(power_fig, width='stretch')

    with st.expander("Thermal", expanded=False):
        st.markdown("<h4 style='text-align: center;'>Thermal</h4>", unsafe_allow_html=True)
        thermal_fig = px.line(df_plot, x="timestamp", y=["obc_temp_c", "eps_batt_temp_c"])
        st.plotly_chart(thermal_fig, width='stretch')

    with st.expander("Attitude Error", expanded=False):
        st.markdown("<h4 style='text-align: center;'>Attitude Error</h4>", unsafe_allow_html=True)
        adcs_fig = px.line(df_plot, x="timestamp", y="adcs_attitude_error_deg")
        st.plotly_chart(adcs_fig, width='stretch')

    with st.expander("Signal Strength", expanded=False):
        st.markdown("<h4 style='text-align: center;'>Signal Strength</h4>", unsafe_allow_html=True)
        rssi_fig = px.line(df_plot, x="timestamp", y="comms_rssi_dbm")
        st.plotly_chart(rssi_fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><p class="panel-title">ANOMALY LOG</p>', unsafe_allow_html=True)
    anomalies = df[df["mode"].isin(["WARNING", "CRITICAL"])]
    if len(anomalies) == 0:
        st.write("No anomalies detected.")
    else:
        st.dataframe(anomalies, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><p class="panel-title">TELEMETRY LOG</p>', unsafe_allow_html=True)
    st.dataframe(df, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)