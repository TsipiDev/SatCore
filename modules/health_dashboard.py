import streamlit as st
import pandas as pd
import plotly.express as px


def get_status(value, warn_low, crit_low, warn_high=None, crit_high=None):
    if value <= crit_low:
        return "critical", "CRITICAL"
    elif crit_high and value >= crit_high:
        return "critical", "CRITICAL"
    elif value <= warn_low:
        return "warning", "WARNING"
    elif warn_high and value >= warn_high:
        return "warning", "WARNING"
    return "nominal", "NOMINAL"


def render():
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
    .nominal { animation: glow 2s infinite; color: #00FFB2; font-weight: bold; font-size: 1.1rem; }
    .warning { animation: slow-flash 1.2s infinite; color: #FFD700; font-weight: bold; font-size: 1.1rem; }
    .critical { animation: fast-flash 0.4s infinite; color: #FF4444; font-weight: bold; font-size: 1.1rem; }
    .metric-nominal { animation: glow 2s infinite; color: #00FFB2; font-size: 1rem; }
    .metric-warning { animation: slow-flash 1.2s infinite; color: #FFD700; font-size: 1rem; }
    .metric-critical { animation: fast-flash 0.4s infinite; color: #FF4444; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

    df = pd.read_csv("data/telemetry/sample_telemetry.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp", ascending=False)

    df["eps_solar_current_a"] = df["eps_solar_current_ma"] / 1000

    latest = df.iloc[0]

    batt_v_class, _ = get_status(latest["eps_batt_voltage_v"], 7.2, 6.8)
    batt_t_class, _ = get_status(latest["eps_batt_temp_c"], 0, -5, 30, 40)
    solar_v_class, _ = get_status(latest["eps_solar_voltage_v"], 4.5, 4.0)
    solar_i_class, _ = get_status(latest["eps_solar_current_ma"], 1200, 900)
    obc_temp_class, _ = get_status(latest["obc_temp_c"], 0, -5, 40, 50)
    adcs_class, _ = get_status(latest["adcs_attitude_error_deg"], -1, -1, 0.3, 0.7)
    rssi_class, _ = get_status(latest["comms_rssi_dbm"], -90, -100)

    st.subheader("Spacecraft Status")

    c1, c2, c3 = st.columns(3)
    c1.metric("Mission Mode", latest["mode"])
    c2.metric("ADCS Mode", latest["adcs_mode"])
    c3.metric("Uptime", f"{latest['obc_uptime_s']} s")

    st.markdown(f"""
    <p>Power: <span class="{batt_v_class}">{batt_v_class.upper()}</span> &nbsp;&nbsp;|&nbsp;&nbsp; Thermal: <span class="{obc_temp_class}">{obc_temp_class.upper()}</span></p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.caption("Power")
    p1, p2, p3, p4 = st.columns(4)
    p1.markdown(f'<p class="metric-{batt_v_class}">Batt Voltage<br><span style="font-size:1.8rem; font-weight:600;">{latest["eps_batt_voltage_v"]:.2f} V</span></p>', unsafe_allow_html=True)
    p2.markdown(f'<p class="metric-{batt_t_class}">Batt Temp<br><span style="font-size:1.8rem; font-weight:600;">{latest["eps_batt_temp_c"]:.1f} C</span></p>', unsafe_allow_html=True)
    p3.markdown(f'<p class="metric-{solar_v_class}">Solar Voltage<br><span style="font-size:1.8rem; font-weight:600;">{latest["eps_solar_voltage_v"]:.2f} V</span></p>', unsafe_allow_html=True)
    p4.markdown(f'<p class="metric-{solar_i_class}">Solar Current<br><span style="font-size:1.8rem; font-weight:600;">{latest["eps_solar_current_ma"]:.0f} mA</span></p>', unsafe_allow_html=True)

    st.markdown("---")

    st.caption("Systems")
    s1, s2, s3 = st.columns(3)
    s1.markdown(f'<p class="metric-{obc_temp_class}">OBC Temp<br><span style="font-size:1.8rem; font-weight:600;">{latest["obc_temp_c"]:.1f} C</span></p>', unsafe_allow_html=True)
    s2.markdown(f'<p class="metric-{adcs_class}">Attitude Error<br><span style="font-size:1.8rem; font-weight:600;">{latest["adcs_attitude_error_deg"]:.2f} deg</span></p>', unsafe_allow_html=True)
    s3.markdown(f'<p class="metric-{rssi_class}">Signal (RSSI)<br><span style="font-size:1.8rem; font-weight:600;">{latest["comms_rssi_dbm"]:.1f} dBm</span></p>', unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("Telemetry Charts")

    st.markdown("<h4 style='text-align: center;'>Power</h4>", unsafe_allow_html=True)
    power_fig = px.line(df.sort_values("timestamp"), x="timestamp", y=["eps_batt_voltage_v", "eps_solar_current_a"])
    st.plotly_chart(power_fig, width='stretch')

    st.markdown("<h4 style='text-align: center;'>Thermal</h4>", unsafe_allow_html=True)
    thermal_fig = px.line(df.sort_values("timestamp"), x="timestamp", y=["obc_temp_c", "eps_batt_temp_c"])
    st.plotly_chart(thermal_fig, width='stretch')

    st.markdown("<h4 style='text-align: center;'>Attitude Error</h4>", unsafe_allow_html=True)
    adcs_fig = px.line(df.sort_values("timestamp"), x="timestamp", y="adcs_attitude_error_deg")
    st.plotly_chart(adcs_fig, width='stretch')

    st.markdown("<h4 style='text-align: center;'>Signal Strength</h4>", unsafe_allow_html=True)
    rssi_fig = px.line(df.sort_values("timestamp"), x="timestamp", y="comms_rssi_dbm")
    st.plotly_chart(rssi_fig, width='stretch')

    st.subheader("Anomaly Log")

    anomalies = df[df["mode"].isin(["WARNING", "CRITICAL"])]

    if len(anomalies) == 0:
        st.write("No anomalies detected.")
    else:
        st.dataframe(anomalies, hide_index=True)

    st.subheader("Telemetry Log")
    st.dataframe(df, hide_index=True)