import streamlit as st
import pandas as pd


def render():
    st.subheader("Data Import")

    uploaded_file = st.file_uploader("Upload Telemetry CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview:")
        st.dataframe(df.head(), hide_index=True)
        st.write(f"Detected columns: {list(df.columns)}")

        st.markdown("---")
        st.write("Map your columns to SatCore parameters")
        st.caption("Only map the parameters available in your CSV. Unmapped parameters will show as Not Provided.")

        satcore_params = [
            "timestamp",
            "eps_batt_voltage_v",
            "eps_batt_temp_c",
            "eps_solar_voltage_v",
            "eps_solar_current_ma",
            "obc_temp_c",
            "obc_uptime_s",
            "adcs_attitude_error_deg",
            "adcs_mode",
            "comms_rssi_dbm",
            "comms_freq_mhz",
            "mode"
        ]

        user_columns = ["-- not mapped --"] + list(df.columns)
        mapping = {}

        for param in satcore_params:
            selected = st.selectbox(f"{param}", user_columns, index=0)
            mapping[param] = None if selected == "-- not mapped --" else selected

        st.markdown("---")

        if st.button("Import Data"):
            normalized = pd.DataFrame()

            for param, col in mapping.items():
                if col is not None:
                    normalized[param] = df[col]
                else:
                    normalized[param] = "Not Provided"

            normalized.to_csv("data/telemetry/sample_telemetry.csv", index=False)
            st.success("Data imported successfully! Redirecting to Health Dashboard...")
            st.session_state["page"] = "Health Dashboard"
            st.rerun()
    else:
        st.info("Upload a CSV file to get started.")