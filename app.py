import streamlit as st
import pandas as pd

st.title("SatCore")

df = pd.read_csv("data/telemetry/sample_telemetry.csv")

st.subheader("Telemetry Data")
st.dataframe(df)