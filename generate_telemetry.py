import pandas as pd
import numpy as np
from datetime import datetime, timedelta

start = datetime(2024, 1, 15, 0, 0, 0)
rows = []

for i in range(2016):
    t = start + timedelta(minutes=5 * i)
    
    # satellites orbit every ~90 mins so battery cycles with that
    orbit_phase = (i % 18) / 18
    in_eclipse = orbit_phase > 0.6
    
    batt_voltage = 8.2 - (0.8 * orbit_phase) + np.random.normal(0, 0.05)
    solar_voltage = 0.0 if in_eclipse else 5.1 + np.random.normal(0, 0.1)
    solar_current = 0.0 if in_eclipse else 1450 + np.random.normal(0, 50)
    batt_temp = 18 + (4 * orbit_phase) + np.random.normal(0, 0.3)
    obc_temp = 23 + (3 * orbit_phase) + np.random.normal(0, 0.2)
    attitude_error = abs(np.random.normal(0.1, 0.05))
    rssi = -87 + np.random.normal(0, 2)
    uptime = 3600 + (i * 300)
    adcs_mode = "NOMINAL"
    mode = "NOMINAL"

    # inject a few anomaly periods
    if 500 <= i <= 520:
        batt_voltage -= 1.5
        mode = "WARNING"
    if 510 <= i <= 515:
        batt_voltage -= 2.0
        mode = "CRITICAL"
    if 1200 <= i <= 1210:
        attitude_error += 0.6
        adcs_mode = "DETUMBLING"
        mode = "WARNING"

    rows.append({
        "timestamp": t,
        "eps_batt_voltage_v": round(batt_voltage, 2),
        "eps_batt_temp_c": round(batt_temp, 1),
        "eps_solar_voltage_v": round(solar_voltage, 2),
        "eps_solar_current_ma": round(solar_current, 0),
        "obc_temp_c": round(obc_temp, 1),
        "obc_uptime_s": uptime,
        "adcs_attitude_error_deg": round(attitude_error, 3),
        "adcs_mode": adcs_mode,
        "comms_rssi_dbm": round(rssi, 1),
        "comms_freq_mhz": 437.5,
        "mode": mode
    })

df = pd.DataFrame(rows)
df.to_csv("data/telemetry/sample_telemetry.csv", index=False)
print(f"generated {len(df)} rows")