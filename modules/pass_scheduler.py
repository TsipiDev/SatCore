import streamlit as st
import requests
from skyfield.api import load, EarthSatellite, wgs84
from datetime import datetime, timezone
import pandas as pd
import pytz


def render():
    st.subheader("Pass Scheduler")

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

    selected_tz = st.selectbox("Display Timezone", list(tz_options.keys()), index=14)
    local_tz = pytz.timezone(tz_options[selected_tz])

    url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=59141&FORMAT=TLE"
    response = requests.get(url)
    lines = response.text.strip().splitlines()

    ts = load.timescale()
    satellite = EarthSatellite(lines[1], lines[2], lines[0], ts)

    st.write(f"Tracking: {lines[0].strip()}")
    st.write(f"Epoch: {satellite.epoch.utc_iso()}")

    ground_station = wgs84.latlon(38.5731, 23.5880)

    t0 = ts.now()
    t1 = ts.tt_jd(t0.tt + 7)

    t, events = satellite.find_events(ground_station, t0, t1, altitude_degrees=10.0)

    passes = []
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
            action = "Prime data transfer window"
        elif alt.degrees >= 30:
            quality = "Good"
            action = "Suitable for telemetry uplink"
        else:
            quality = "Marginal"
            action = "Command only, avoid bulk transfer"

        rise_local = rise_time.astimezone(local_tz)
        peak_local = peak_time.astimezone(local_tz)
        set_local = set_time.astimezone(local_tz)

        pass_windows.append({
            "AOS": rise_local.strftime("%Y-%m-%d %H:%M:%S"),
            "TCA": peak_local.strftime("%H:%M:%S"),
            "LOS": set_local.strftime("%H:%M:%S"),
            "Duration (mins)": duration,
            "Max Elevation (deg)": round(alt.degrees, 1),
            "Quality": quality,
            "Recommended Action": action
        })

    next_pass = pass_windows[0]
    now = datetime.now(timezone.utc)
    next_aos = datetime.fromisoformat(passes[0]["time"].replace("Z", "+00:00"))
    time_until = next_aos - now
    hours = int(time_until.total_seconds() // 3600)
    mins = int((time_until.total_seconds() % 3600) // 60)

    st.write("Next Pass")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AOS", next_pass["AOS"].split(" ")[1])
    c2.metric("Quality", next_pass["Quality"])
    c3.metric("Max Elevation", f"{next_pass['Max Elevation (deg)']} deg")
    c4.metric("Time Until Pass", f"{hours}h {mins}m")

    st.markdown("---")
    st.write("Upcoming Passes")

    df_passes = pd.DataFrame(pass_windows)
    st.dataframe(df_passes, hide_index=True)
