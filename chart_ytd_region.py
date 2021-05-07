from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, Div, Panel
from bokeh.layouts import layout, column, row
from data import groupings, dataframe,  transform_inputs
from classPeriodAmounts import PeriodAmounts
from widgets import button_group_area4, button_group_qtr4, button_group_yr4, options_qtr4, options_yr4, options_area4
#from bar_chart import create_chart

from bokeh.io import curdoc
from bokeh.models import Tabs
from bokeh.models import FactorRange #requires list of string tuples 
from bokeh.plotting import figure
from bokeh.models import Range1d, LinearAxis


def create_chart(factors, source):

    p = figure(x_range=FactorRange(*factors), plot_height=350,
        toolbar_location=None, tools="")

    #p.vbar_stack(area, x='x', width=0.9, color=colors, source=source, legend_label=area)

    p.vbar(x='x', top='y', width=0.9, alpha=0.5, source=source)
    p.y_range.start = 0

    p.extra_y_ranges = {"Subscribers": Range1d(start=0, end=100)}
    p.triangle(x='x', y='y_subs', color="red", line_width=2, y_range_name="Subscribers", size=7, alpha=0.50, source=source)
    p.add_layout(LinearAxis(y_range_name="Subscribers"), 'right')

    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None

    return p


def update_chart(attr, old ,new):
    qtrs = []
    years = []
    areas = []

    for i in button_group_qtr4.active:
        qtrs.append(int(options_qtr4[i]))

    for i in button_group_yr4.active:
        years.append(int(options_yr4[i]))
    
    for i in button_group_area4.active:
        areas.append(options_area4[i])
          
    factors, params_chart = transform_inputs(qtrs, years, areas)

    try:
        #when qtr, yr, AND area are selected 
        params_chart[0][2]
        p.x_range.factors = factors
        y_rev, y_subs = chart1_data.get_ytd(params_chart)
        source.data = {
            'x': factors,
            'y': y_rev,
            'y_subs': y_subs
        }
    except:
        source.data = {
            'x': [],
            'y': [],
            'y_subs': []
        }
        #p.x_range.factors = []
    print('UPDATED SOURCE', source.data)



button_group_yr4.on_change("active",update_chart)
button_group_qtr4.on_change("active",update_chart)
button_group_area4.on_change("active",update_chart)

#CREATE CHART FOR BY QTR AND BY YEAR
#starting params in chart, widgets only takes a list of strings
factors, params_chart = transform_inputs(['1','2','3','4'], ['2018','2019','2020'], ['United States and Canada'])
#instantiate for plotting data with df
chart1_data = PeriodAmounts(dataframe)
rev, subs = chart1_data.get_ytd(params_chart)
source = ColumnDataSource(data=dict(x=factors, y=rev, y_subs=subs))
p = create_chart(factors, source)
#annotations settings
hover = HoverTool(tooltips=[
    ('qtr,yr','@x'),
    ('qtd revenue','$@y{0.1f} m'), 
    ('subscribers','@y_subs{0.0 a}m')])
p.add_tools(hover)
#first tab
l = column(
    row(p), 
    row(Div(text="<h3>Quarter(s)</h3>"), button_group_qtr4),
    row(Div(text="<h3>Year(s)</h3>"), button_group_yr4),
    row(Div(text="<h3>Region(s)</h3>"), button_group_area4),
    )

tab_ytd_region = Panel(child=l, title="YTD Rev By Region")

#tabs = Tabs(tabs=[ tab_ytd_region ])

#curdoc().add_root(tabs)

