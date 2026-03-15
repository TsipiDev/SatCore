import streamlit as st
import requests
from skyfield.api import load, EarthSatellite, wgs84
from datetime import datetime, timezone


def render():
    st.subheader("Pass Scheduler")

    url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=59141&FORMAT=TLE"
    response = requests.get(url)
    lines = response.text.strip().splitlines()

    ts = load.timescale()
    satellite = EarthSatellite(lines[1], lines[2], lines[0], ts)

    st.write(f"Tracking: {lines[0].strip()}")
    st.write(f"Epoch: {satellite.epoch.utc_iso()}")

    ts = load.timescale()

    ground_station = wgs84.latlon(38.5731, 23.5880)

    t0 = ts.now()
    t1 = ts.tt_jd(t0.tt + 1)

    passes = []

    difference = satellite - ground_station
    t, events = satellite.find_events(ground_station, t0, t1, altitude_degrees=10.0)

    for ti, event in zip(t, events):
        event_name = ["rise", "peak", "set"][event]
        passes.append({
            "time": ti.utc_iso(),
            "event": event_name,
            "name": lines[0].strip()
        })

    st.write(passes)
