from utils.styles import load_css
from utils.styles import load_sidebar
from modules import pass_scheduler
load_css()
load_sidebar("Pass_Scheduler")
pass_scheduler.render()