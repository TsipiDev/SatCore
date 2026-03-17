import streamlit as st
import pandas as pd


def render():

    st.markdown('<p class="page-title">Data Import</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">TELEMETRY CSV IMPORT & PARAMETER MAPPING</p>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><p class="panel-title">UPLOAD</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Telemetry CSV", type="csv")
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.markdown('<div class="panel"><p class="panel-title">PREVIEW</p>', unsafe_allow_html=True)
        st.dataframe(df.head(), hide_index=True)
        st.write(f"Detected columns: {list(df.columns)}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel"><p class="panel-title">PARAMETER MAPPING</p>', unsafe_allow_html=True)
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

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel"><p class="panel-title">IMPORT</p>', unsafe_allow_html=True)
        if st.button("Import Data"):
            normalized = pd.DataFrame()

            for param, col in mapping.items():
                if col is not None:
                    normalized[param] = df[col]
                else:
                    if param in ["adcs_mode", "mode", "timestamp"]:
                        normalized[param] = "Not Provided"
                    else:
                        normalized[param] = 0

            normalized.to_csv("data/telemetry/sample_telemetry.csv", index=False)
            st.success("Data imported successfully! Navigate to Health Dashboard to view.")
            st.session_state["page"] = "Health Dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="panel"><p class="panel-title">INSTRUCTIONS</p>', unsafe_allow_html=True)
        st.write("Upload a decoded telemetry CSV file to get started.")
        st.write("Your CSV can use any column names — you will map them to SatCore parameters in the next step.")
        st.write("Parameters that are not mapped will display as Not Provided across all modules.")
        st.markdown('</div>', unsafe_allow_html=True)