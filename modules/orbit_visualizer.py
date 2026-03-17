import streamlit as st
import plotly.graph_objects as go
from skyfield.api import load, EarthSatellite, wgs84
from datetime import datetime, timezone
import os
import time


def render():
    st.subheader("Orbit Visualizer")

    refresh_options = {"10 seconds": 10, "30 seconds": 30, "60 seconds": 60}
    selected_refresh = st.select_slider("Auto Refresh", options=list(refresh_options.keys()), value="30 seconds")
    refresh_secs = refresh_options[selected_refresh]

    if not os.path.exists("data/tle_data/active.tle"):
        st.warning("TLE catalog not found. Please run fetch_tle_catalog.py first.")
        return

    with open("data/tle_data/active.tle") as f:
        catalog_lines = f.read().strip().splitlines()

    clean_lines = [line for line in catalog_lines if line.strip() != ""]
    all_satellites = {}
    for i in range(0, len(clean_lines) - 2, 3):
        name = clean_lines[i].strip()
        all_satellites[name] = clean_lines[i:i+3]

    lines = all_satellites.get("TIGER-7")
    ts = load.timescale()
    satellite = EarthSatellite(lines[1], lines[2], lines[0], ts)

    @st.fragment(run_every=refresh_secs)
    def render_globe():
        now_dt = datetime.now(timezone.utc)
        times = ts.utc(now_dt.year, now_dt.month, now_dt.day,
                       now_dt.hour, range(now_dt.minute, now_dt.minute + 95))

        geocentric = satellite.at(times)
        subpoint = wgs84.subpoint_of(geocentric)

        lats = subpoint.latitude.degrees.tolist()
        lons = subpoint.longitude.degrees.tolist()

        now = ts.now()
        current = satellite.at(now)
        current_pos = wgs84.subpoint_of(current)

        fig = go.Figure()

        fig.add_trace(go.Scattergeo(
            lat=lats,
            lon=lons,
            mode="lines",
            line=dict(color="#00FFB2", width=2),
            name="Orbital Track"
        ))

        fig.add_trace(go.Scattergeo(
            lat=[current_pos.latitude.degrees],
            lon=[current_pos.longitude.degrees],
            mode="markers",
            marker=dict(size=10, color="#FF4444", symbol="circle"),
            name="TIGER-7"
        ))

        fig.add_trace(go.Scattergeo(
            lat=[38.5731],
            lon=[23.5880],
            mode="markers+text",
            marker=dict(size=8, color="#FFD700", symbol="triangle-up"),
            text=["Psahna GS"],
            textposition="top right",
            name="Ground Station"
        ))

        fig.update_geos(
            projection_type="orthographic",
            showland=True,
            landcolor="#1a1a2e",
            showocean=True,
            oceancolor="#0a0a1a",
            showcoastlines=True,
            coastlinecolor="#333366",
            bgcolor="#0E1117"
        )

        fig.update_layout(
            template="plotly_dark",
            height=600,
            margin=dict(t=0, b=0, l=0, r=0),
            geo=dict(bgcolor="#0E1117")
        )

        st.plotly_chart(fig)

    render_globe()