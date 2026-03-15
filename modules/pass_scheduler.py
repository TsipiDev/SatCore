import streamlit as st
import requests
from skyfield.api import load, EarthSatellite, wgs84
from datetime import datetime
import pandas as pd

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
    t1 = ts.tt_jd(t0.tt + 7)

    passes = []

    t, events = satellite.find_events(ground_station, t0, t1, altitude_degrees=10.0)

    for ti, event in zip(t, events):
        event_name = ["rise", "peak", "set"][event]
        passes.append({
            "time": ti.utc_iso(),
            "event": event_name,
            "name": lines[0].strip()
        })

    pass_windows = []
    for i in range(0, len(passes) - 2, 3):
        rise = passes[i]
        peak = passes[i+1]
        set_ = passes[i+2]

        rise_time = datetime.fromisoformat(rise["time"].replace("Z", "+00:00"))
        peak_time = datetime.fromisoformat(peak["time"].replace("Z", "+00:00"))
        set_time = datetime.fromisoformat(set_["time"].replace("Z", "+00:00"))

        duration = round((set_time - rise_time).total_seconds() / 60, 1)

        peak_t = t[i+1]
        difference = satellite - ground_station
        topocentric = difference.at(peak_t)
        alt, _, _ = topocentric.altaz()

        
        if alt.degrees >= 60:
            quality = "Excellent"
        elif alt.degrees >= 30:
            quality = "Good"
        else:
            quality = "Marginal"

        pass_windows.append({
            "Rise": rise_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "Peak": peak_time.strftime("%H:%M:%S UTC"),
            "Set": set_time.strftime("%H:%M:%S UTC"),
            "Duration (mins)": duration,
            "Max Elevation (deg)": round(alt.degrees, 1),
            "Quality": quality
        })

    df_passes = pd.DataFrame(pass_windows)
    st.dataframe(df_passes, hide_index=True)
