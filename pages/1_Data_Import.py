from utils.styles import load_css
from utils.styles import load_sidebar
from modules import data_import
load_css()
load_sidebar("Data_Import")
data_import.render()