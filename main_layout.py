from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import Panel, Tabs
from chart_qtd import tab_qtd
from chart_ytd import tab_ytd
from chart_qtd_region import tab_qtd_region
from chart_ytd_region import tab_ytd_region
from chart_ytd_region_stacked import tab_ytd_stacked


tabs = Tabs(tabs=[ tab_qtd, tab_ytd, tab_ytd_stacked, tab_qtd_region, tab_ytd_region ])

curdoc().add_root(tabs)