import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def render():
    st.markdown("""
    <style>
    @keyframes glow {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    .nominal { animation: glow 2s infinite; color: #00FFB2; font-weight: bold; }
    .warning { animation: glow 2s infinite; color: #FFD700; font-weight: bold; }
    .critical { animation: glow 2s infinite; color: #FF4444; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Telemetry Analyzer")

    df = pd.read_csv("data/telemetry/sample_telemetry.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    latest = df.iloc[-1]

    anomalies = df[df["mode"] != "NOMINAL"].copy()
    if len(anomalies) > 0:
        anomalies["event"] = (anomalies["timestamp"].diff() > pd.Timedelta(minutes=5)).cumsum()
        events = []
        for event_id, group in anomalies.groupby("event"):
            events.append({
                "start": group["timestamp"].iloc[0],
                "end": group["timestamp"].iloc[-1],
                "duration_mins": round((group["timestamp"].iloc[-1] - group["timestamp"].iloc[0]).total_seconds() / 60),
                "max_severity": group["mode"].max(),
                "rows": len(group)
            })
        events_df = pd.DataFrame(events)
        num_events = len(events_df)
    else:
        events_df = None
        num_events = 0

    warn_count = 0
    crit_count = 0

    if latest["eps_batt_voltage_v"] < 6.8:
        crit_count += 1
    elif latest["eps_batt_voltage_v"] < 7.2:
        warn_count += 1

    if latest["eps_batt_temp_c"] > 40:
        crit_count += 1
    elif latest["eps_batt_temp_c"] > 30:
        warn_count += 1

    if latest["obc_temp_c"] > 50:
        crit_count += 1
    elif latest["obc_temp_c"] > 40:
        warn_count += 1

    if latest["comms_rssi_dbm"] < -100:
        crit_count += 1
    elif latest["comms_rssi_dbm"] < -90:
        warn_count += 1

    if latest["adcs_attitude_error_deg"] > 0.7:
        crit_count += 1
    elif latest["adcs_attitude_error_deg"] > 0.3:
        warn_count += 1

    if crit_count > 0:
        overall = "CRITICAL"
        overall_class = "critical"
    elif warn_count >= 2:
        overall = "DEGRADED"
        overall_class = "warning"
    elif warn_count == 1:
        overall = "WARNING"
        overall_class = "warning"
    else:
        overall = "NOMINAL"
        overall_class = "nominal"

    st.write("Spacecraft Overview")
    o1, o2, o3 = st.columns(3)
    o1.markdown(f'<p>Overall Health<br><span class="{overall_class}" style="font-size:1.8rem;">{overall}</span></p>', unsafe_allow_html=True)
    o2.metric("Anomaly Events", num_events)
    o3.metric("Observation Period", "7 days")

    st.markdown("---")

    total = len(df)
    mode_counts = df["mode"].value_counts()

    nominal_pct = round((mode_counts.get("NOMINAL", 0) / total) * 100, 1)
    warning_pct = round((mode_counts.get("WARNING", 0) / total) * 100, 1)
    critical_pct = round((mode_counts.get("CRITICAL", 0) / total) * 100, 1)

    st.write("Mission Health Summary")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<p>Nominal<br><span class="nominal" style="font-size:1.8rem;">{nominal_pct}%</span></p>', unsafe_allow_html=True)
    c2.markdown(f'<p>Warning<br><span class="warning" style="font-size:1.8rem;">{warning_pct}%</span></p>', unsafe_allow_html=True)
    c3.markdown(f'<p>Critical<br><span class="critical" style="font-size:1.8rem;">{critical_pct}%</span></p>', unsafe_allow_html=True)

    st.markdown("---")
    st.write("Anomaly Events")

    if events_df is None:
        st.write("No anomalies detected.")
    else:
        for i, row in events_df.iterrows():
            st.markdown(f"**Event {i+1}** — {row['start'].strftime('%Y-%m-%d %H:%M')} to {row['end'].strftime('%Y-%m-%d %H:%M')}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Duration", f"{row['duration_mins']} mins")
            severity_class = row['max_severity'].lower()
            c2.markdown(f'<p>Severity<br><span class="{severity_class}" style="font-size:1.8rem;">{row["max_severity"]}</span></p>', unsafe_allow_html=True)
            c3.metric("Readings affected", row['rows'])

            window = df[(df["timestamp"] >= row["start"]) & (df["timestamp"] <= row["end"])]

            causes = []
            if window["eps_batt_voltage_v"].min() < 6.8:
                causes.append("low battery voltage")
            if window["eps_batt_temp_c"].max() > 40:
                causes.append("high battery temperature")
            if window["obc_temp_c"].max() > 50:
                causes.append("high OBC temperature")
            if window["adcs_attitude_error_deg"].max() > 0.7:
                causes.append("attitude error exceeded limit")
            if window["comms_rssi_dbm"].min() < -100:
                causes.append("signal loss")

            if causes:
                st.write(f"Possible cause: {', '.join(causes)}")
            else:
                st.write("Cause could not be determined from available data.")

            st.markdown("---")

    st.markdown("---")
    st.write("Parameter Trend Forecast")

    df["timestamp_num"] = (df["timestamp"] - df["timestamp"].min()).dt.total_seconds()
    df_plot = df.sort_values("timestamp").set_index("timestamp").resample("6h").mean(numeric_only=True).reset_index()

    future_days = 30
    future_seconds = [df["timestamp_num"].max() + i * 86400 for i in range(future_days)]
    future_timestamps = [df["timestamp"].max() + pd.Timedelta(days=i) for i in range(future_days)]

    # Battery Voltage
    coeffs = np.polyfit(df["timestamp_num"], df["eps_batt_voltage_v"], 1)
    slope_per_day = coeffs[0] * 86400
    future_values = [coeffs[1] + coeffs[0] * s for s in future_seconds]

    with st.expander("Battery Voltage", expanded=True):
        if slope_per_day < 0:
            days_to_warn = (df["eps_batt_voltage_v"].iloc[-1] - 7.2) / abs(slope_per_day)
            st.markdown(f'<span class="warning">Declining — WARNING estimated in {days_to_warn:.1f} days</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="nominal">Stable — trend: {slope_per_day:.4f} V/day</span>', unsafe_allow_html=True)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df_plot["timestamp"], y=df_plot["eps_batt_voltage_v"], name="Actual", mode="lines+markers", line=dict(color="#00FFB2")))
        fig1.add_trace(go.Scatter(x=future_timestamps, y=future_values, name="Forecast", line=dict(color="#FFD700", dash="dash")))
        fig1.add_hline(y=7.2, line_color="#FF4444", line_dash="dot", annotation_text="WARNING")
        fig1.update_layout(template="plotly_dark", title="Battery Voltage Forecast", height=300, margin=dict(t=40), yaxis=dict(range=[6.5, 9.0]))
        st.plotly_chart(fig1)

    # OBC Temperature
    coeffs = np.polyfit(df["timestamp_num"], df["obc_temp_c"], 1)
    slope_per_day = coeffs[0] * 86400
    future_values = [coeffs[1] + coeffs[0] * s for s in future_seconds]

    with st.expander("OBC Temperature", expanded=True):
        if slope_per_day > 0:
            days_to_warn = (40 - df["obc_temp_c"].iloc[-1]) / slope_per_day
            st.markdown(f'<span class="warning">Rising — WARNING estimated in {days_to_warn:.1f} days</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="nominal">Stable — trend: {slope_per_day:.4f} C/day</span>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df_plot["timestamp"], y=df_plot["obc_temp_c"], name="Actual", mode="lines+markers", line=dict(color="#00FFB2")))
        fig2.add_trace(go.Scatter(x=future_timestamps, y=future_values, name="Forecast", line=dict(color="#FFD700", dash="dash")))
        fig2.add_hline(y=40, line_color="#FF4444", line_dash="dot", annotation_text="WARNING")
        fig2.update_layout(template="plotly_dark", title="OBC Temperature Forecast", height=300, margin=dict(t=40), yaxis=dict(range=[15, 55]))
        st.plotly_chart(fig2)

    # Battery Temperature
    coeffs = np.polyfit(df["timestamp_num"], df["eps_batt_temp_c"], 1)
    slope_per_day = coeffs[0] * 86400
    future_values = [coeffs[1] + coeffs[0] * s for s in future_seconds]

    with st.expander("Battery Temperature", expanded=True):
        if slope_per_day > 0:
            days_to_warn = (30 - df["eps_batt_temp_c"].iloc[-1]) / slope_per_day
            st.markdown(f'<span class="warning">Rising — WARNING estimated in {days_to_warn:.1f} days</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="nominal">Stable — trend: {slope_per_day:.4f} C/day</span>', unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_plot["timestamp"], y=df_plot["eps_batt_temp_c"], name="Actual", mode="lines+markers", line=dict(color="#00FFB2")))
        fig3.add_trace(go.Scatter(x=future_timestamps, y=future_values, name="Forecast", line=dict(color="#FFD700", dash="dash")))
        fig3.add_hline(y=30, line_color="#FF4444", line_dash="dot", annotation_text="WARNING")
        fig3.update_layout(template="plotly_dark", title="Battery Temperature Forecast", height=300, margin=dict(t=40), yaxis=dict(range=[10, 45]))
        st.plotly_chart(fig3)

    # Signal Strength
    coeffs = np.polyfit(df["timestamp_num"], df["comms_rssi_dbm"], 1)
    slope_per_day = coeffs[0] * 86400
    future_values = [coeffs[1] + coeffs[0] * s for s in future_seconds]

    with st.expander("Signal Strength", expanded=True):
        if slope_per_day < 0:
            days_to_warn = (df["comms_rssi_dbm"].iloc[-1] - (-90)) / abs(slope_per_day)
            st.markdown(f'<span class="warning">Declining — WARNING estimated in {days_to_warn:.1f} days</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="nominal">Stable — trend: {slope_per_day:.4f} dBm/day</span>', unsafe_allow_html=True)
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=df_plot["timestamp"], y=df_plot["comms_rssi_dbm"], name="Actual", mode="lines+markers", line=dict(color="#00FFB2")))
        fig4.add_trace(go.Scatter(x=future_timestamps, y=future_values, name="Forecast", line=dict(color="#FFD700", dash="dash")))
        fig4.add_hline(y=-90, line_color="#FF4444", line_dash="dot", annotation_text="WARNING")
        fig4.update_layout(template="plotly_dark", title="Signal Strength Forecast", height=300, margin=dict(t=40), yaxis=dict(range=[-100, -75]))
        st.plotly_chart(fig4)

    # Attitude Error
    coeffs = np.polyfit(df["timestamp_num"], df["adcs_attitude_error_deg"], 1)
    slope_per_day = coeffs[0] * 86400
    future_values = [coeffs[1] + coeffs[0] * s for s in future_seconds]

    with st.expander("Attitude Error", expanded=True):
        if slope_per_day > 0:
            days_to_warn = (0.3 - df["adcs_attitude_error_deg"].iloc[-1]) / slope_per_day
            st.markdown(f'<span class="warning">Rising — WARNING estimated in {days_to_warn:.1f} days</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="nominal">Stable — trend: {slope_per_day:.4f} deg/day</span>', unsafe_allow_html=True)
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=df_plot["timestamp"], y=df_plot["adcs_attitude_error_deg"], name="Actual", mode="lines+markers", line=dict(color="#00FFB2")))
        fig5.add_trace(go.Scatter(x=future_timestamps, y=future_values, name="Forecast", line=dict(color="#FFD700", dash="dash")))
        fig5.add_hline(y=0.3, line_color="#FF4444", line_dash="dot", annotation_text="WARNING")
        fig5.update_layout(template="plotly_dark", title="Attitude Error Forecast", height=300, margin=dict(t=40), yaxis=dict(range=[0, 1.0]))
        st.plotly_chart(fig5)