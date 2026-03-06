import streamlit as st
import pandas as pd


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

    anomalies = df[df["mode"] != "NOMINAL"].copy()

    if len(anomalies) == 0:
        st.write("No anomalies detected.")
    else:
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