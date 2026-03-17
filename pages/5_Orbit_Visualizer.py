from utils.styles import load_css
from utils.styles import load_sidebar
from modules import orbit_visualizer
load_css()
load_sidebar("Orbit_Visualizer")
orbit_visualizer.render()