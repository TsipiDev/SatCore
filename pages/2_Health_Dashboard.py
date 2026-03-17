from utils.styles import load_css
from utils.styles import load_sidebar
from modules import health_dashboard
load_css()
load_sidebar("Health_Dashboard")
health_dashboard.render()