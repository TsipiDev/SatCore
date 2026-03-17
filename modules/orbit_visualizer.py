import streamlit as st
import plotly.graph_objects as go
from skyfield.api import load, EarthSatellite, wgs84
import os


def render():
    st.subheader("Orbit Visualizer")

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

    # calculate one full orbit (90 mins)
    times = ts.utc(2026, 3, 17, 0, range(0, 95))
    geocentric = satellite.at(times)
    subpoint = wgs84.subpoint_of(geocentric)

    lats = subpoint.latitude.degrees.tolist()
    lons = subpoint.longitude.degrees.tolist()

    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lat=lats,
        lon=lons,
        mode="lines",
        line=dict(color="#00FFB2", width=2),
        name="Orbital Track"
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