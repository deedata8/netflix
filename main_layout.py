from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import Panel, Tabs
from chart_qtd import tab_qtd
from chart_ytd import tab_ytd
from chart_qtd_region import tab_qtd_region
from chart_ytd_region import tab_ytd_region
from chart_ytd_region_stacked import tab_ytd_stacked
from csv_dl import main 

#bokeh serve main_layout.py

tabs = Tabs(tabs=[ tab_qtd, tab_ytd, tab_qtd_region, tab_ytd_region, tab_ytd_stacked, main.csv_dl ])

curdoc().add_root(tabs)