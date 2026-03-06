import streamlit as st
import pandas as pd


def render():
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
    c1.metric("Nominal", f"{nominal_pct}%")
    c2.metric("Warning", f"{warning_pct}%")
    c3.metric("Critical", f"{critical_pct}%")