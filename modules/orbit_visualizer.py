import streamlit as st
import plotly.graph_objects as go
from skyfield.api import load, EarthSatellite, wgs84
from datetime import datetime, timezone
import os
import json
import pytz


def render():

    st.markdown('<p class="page-title">Orbit Visualizer</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">REAL-TIME 3D ORBITAL TRACK & POSITION VISUALIZATION</p>', unsafe_allow_html=True)

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

    with open("data/ground_stations.json") as f:
        ground_stations = json.load(f)

    tz_options = {
        "UTC-12": "Etc/GMT+12",
        "UTC-11": "Etc/GMT+11",
        "UTC-10": "Etc/GMT+10",
        "UTC-9": "Etc/GMT+9",
        "UTC-8": "Etc/GMT+8",
        "UTC-7": "Etc/GMT+7",
        "UTC-6": "Etc/GMT+6",
        "UTC-5": "Etc/GMT+5",
        "UTC-4": "Etc/GMT+4",
        "UTC-3": "Etc/GMT+3",
        "UTC-2": "Etc/GMT+2",
        "UTC-1": "Etc/GMT+1",
        "UTC": "UTC",
        "UTC+1": "Etc/GMT-1",
        "UTC+2": "Etc/GMT-2",
        "UTC+3": "Etc/GMT-3",
        "UTC+4": "Etc/GMT-4",
        "UTC+5": "Etc/GMT-5",
        "UTC+6": "Etc/GMT-6",
        "UTC+7": "Etc/GMT-7",
        "UTC+8": "Etc/GMT-8",
        "UTC+9": "Etc/GMT-9",
        "UTC+10": "Etc/GMT-10",
        "UTC+11": "Etc/GMT-11",
        "UTC+12": "Etc/GMT-12",
        "UTC+13": "Etc/GMT-13",
        "UTC+14": "Etc/GMT-14"
    }

    st.markdown('<div class="panel"><p class="panel-title">CONFIGURATION</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        gs_names = [gs["name"] for gs in ground_stations]
        selected_gs_name = st.selectbox("Ground Station", gs_names, index=0)
        selected_gs = next(gs for gs in ground_stations if gs["name"] == selected_gs_name)

    with col2:
        sat_names = list(all_satellites.keys())
        selected_satellite = st.selectbox("Select Satellite", sat_names, index=sat_names.index("TIGER-7") if "TIGER-7" in sat_names else 0)
        lines = all_satellites[selected_satellite]

    with col3:
        selected_tz = st.selectbox("Display Timezone", list(tz_options.keys()), index=14)
        local_tz = pytz.timezone(tz_options[selected_tz])

    st.markdown('</div>', unsafe_allow_html=True)

    ts = load.timescale()
    satellite = EarthSatellite(lines[1], lines[2], lines[0], ts)
    ground_station = wgs84.latlon(selected_gs["lat"], selected_gs["lon"])

    st.markdown('<div class="panel"><p class="panel-title">TRACKING INFO</p>', unsafe_allow_html=True)
    st.metric("Satellite", lines[0].strip())
    st.metric("Ground Station", selected_gs["name"])
    st.metric("TLE Epoch", satellite.epoch.utc_iso().replace("T", " ").replace("Z", " UTC"))
    st.markdown('</div>', unsafe_allow_html=True)

    t0 = ts.now()
    t1 = ts.tt_jd(t0.tt + 7)
    t, events = satellite.find_events(ground_station, t0, t1, altitude_degrees=10.0)

    passes = []
    for ti, event in zip(t, events):
        passes.append({
            "time": ti.utc_iso(),
            "event": ["rise", "peak", "set"][event]
        })

    if len(passes) >= 3:
        rise_time = datetime.fromisoformat(passes[0]["time"].replace("Z", "+00:00"))
        peak_time = datetime.fromisoformat(passes[1]["time"].replace("Z", "+00:00"))
        set_time = datetime.fromisoformat(passes[2]["time"].replace("Z", "+00:00"))
        duration = round((set_time - rise_time).total_seconds() / 60, 1)

        peak_t = t[1]
        diff = satellite - ground_station
        topo = diff.at(peak_t)
        alt, _, _ = topo.altaz()

        rise_local = rise_time.astimezone(local_tz)
        now_utc = datetime.now(timezone.utc)
        time_until = rise_time - now_utc
        hours = int(time_until.total_seconds() // 3600)
        mins = int((time_until.total_seconds() % 3600) // 60)

        st.markdown('<div class="panel"><p class="panel-title">NEXT PASS</p>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("AOS", rise_local.strftime("%H:%M:%S"))
        c2.metric("Duration", f"{duration} mins")
        c3.metric("Max Elevation", f"{round(alt.degrees, 1)} deg")
        c4.metric("Time Until Pass", f"{hours}h {mins}m")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="panel"><p class="panel-title">NEXT PASS</p>', unsafe_allow_html=True)
        st.write("No upcoming passes found in the next 7 days.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><p class="panel-title">ORBITAL TRACK</p>', unsafe_allow_html=True)

    refresh_options = {"10 seconds": 10, "30 seconds": 30, "60 seconds": 60}
    selected_refresh = st.select_slider("Auto Refresh", options=list(refresh_options.keys()), value="30 seconds")
    refresh_secs = refresh_options[selected_refresh]

    @st.fragment(run_every=refresh_secs)
    def render_globe():
        now_dt = datetime.now(timezone.utc)
        mean_motion = float(lines[2].split()[7])
        orbital_period = 1440 / mean_motion
        now = ts.now()
        step = orbital_period / 90
        times = ts.tt_jd([now.tt + (i * step / 1440) for i in range(91)])

        geocentric = satellite.at(times)
        subpoint = wgs84.subpoint_of(geocentric)
        lats = subpoint.latitude.degrees.tolist()
        lons = subpoint.longitude.degrees.tolist()

        current = satellite.at(ts.now())
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
            name=lines[0].strip()
        ))

        fig.add_trace(go.Scattergeo(
            lat=[selected_gs["lat"]],
            lon=[selected_gs["lon"]],
            mode="markers+text",
            marker=dict(size=8, color="#FFD700", symbol="triangle-up"),
            text=[selected_gs["name"]],
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
            bgcolor="#0E1117",
            projection_rotation=dict(
                lon=current_pos.longitude.degrees,
                lat=current_pos.latitude.degrees
            )
        )

        fig.update_layout(
            template="plotly_dark",
            height=600,
            margin=dict(t=0, b=0, l=0, r=0),
            geo=dict(bgcolor="#0E1117")
        )

        st.plotly_chart(fig)

    render_globe()
    st.markdown('</div>', unsafe_allow_html=True)