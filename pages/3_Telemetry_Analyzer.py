from utils.styles import load_css
from utils.styles import load_sidebar
from modules import telemetry_analyzer
load_css()
load_sidebar("Telemetry_Analyzer")
telemetry_analyzer.render()