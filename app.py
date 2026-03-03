import streamlit as st
import pandas as pd

st.title("SatCore 🛰️")

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

latest = df.iloc[-1]

def get_status(value, warn_low, crit_low, warn_high=None, crit_high=None):
    if value <= crit_low:
        return "critical", "🔴 CRITICAL"
    elif crit_high and value >= crit_high:
        return "critical", "🔴 CRITICAL"
    elif value <= warn_low:
        return "warning", "🟡 WARNING"
    elif warn_high and value >= warn_high:
        return "warning", "🟡 WARNING"
    return "nominal", "🟢 NOMINAL"

battery_class, battery_label = get_status(latest["battery_voltage"], 7.2, 6.8)
solar_class, solar_label = get_status(latest["solar_current"], 1.2, 0.9)
temp_class, temp_label = get_status(latest["temperature_obc"], 0, -5, 40, 50)
signal_class, signal_label = get_status(latest["signal_strength"], -90, -100)
attitude_class, attitude_label = get_status(latest["attitude_error"], -1, -1, 0.3, 0.7)


st.subheader("Spacecraft Status")
st.metric("Mission Mode", latest["mode"])

st.markdown(f"""
<p>Power: <span class="{battery_class}">{battery_label}</span> &nbsp;&nbsp;|&nbsp;&nbsp; Thermal: <span class="{temp_class}">{temp_label}</span></p>
""", unsafe_allow_html=True)

st.subheader("Latest Reading")
col1, col2, col3, col4, col5 = st.columns(5)

col1.markdown(f'<p class="metric-{battery_class}">Battery<br><span style="font-size:1.8rem; font-weight:600;">{latest["battery_voltage"]:.2f} V</span></p>', unsafe_allow_html=True)
col2.markdown(f'<p class="metric-{solar_class}">Solar<br><span style="font-size:1.8rem; font-weight:600;">{latest["solar_current"]:.2f} A</span></p>', unsafe_allow_html=True)
col3.markdown(f'<p class="metric-{temp_class}">OBC Temp<br><span style="font-size:1.8rem; font-weight:600;">{latest["temperature_obc"]:.1f} °C</span></p>', unsafe_allow_html=True)
col4.markdown(f'<p class="metric-{signal_class}">Signal<br><span style="font-size:1.8rem; font-weight:600;">{latest["signal_strength"]:.1f} dB</span></p>', unsafe_allow_html=True)
col5.markdown(f'<p class="metric-{attitude_class}">Attitude<br><span style="font-size:1.8rem; font-weight:600;">{latest["attitude_error"]:.2f} °</span></p>', unsafe_allow_html=True)

import plotly.express as px

st.subheader("Battery Voltage Over Time")
fig = px.line(df, x="timestamp", y="battery_voltage")
st.plotly_chart(fig)

st.subheader("Telemetry Log")
st.dataframe(df, hide_index=True)