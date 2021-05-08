from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, Div, Panel
from bokeh.layouts import layout, column, row
from data import groupings, dataframe,  transform_inputs
from classPeriodAmounts import PeriodAmounts
from widgets import button_group_area4, button_group_qtr4, button_group_yr4, options_qtr4, options_yr4, options_area4
from bokeh.transform import factor_cmap
#from bar_chart import create_chart

from bokeh.io import curdoc
from bokeh.models import Tabs
from bokeh.models import FactorRange #requires list of string tuples 
from bokeh.plotting import figure
from bokeh.models import Range1d, LinearAxis


from data import dataframe 
from classPeriodAmounts import PeriodAmounts 

#palette = ["blue", "red"]
#region = ['United States and Canada', 'Latin America']

palette = ["blue", "red", "green", "yellow"]
region = ['United States and Canada', 'Latin America', 'Europe,  Middle East and Africa', 'Asia-Pacific']

def create_chart(factors, source, region, palette):

    print('FROM CREATE CHART', source.data)
    
    p = figure(x_range=FactorRange(*factors), plot_height=250,
            toolbar_location=None, tools="")

    # #stack by region 
    # p.vbar_stack(region, x='x', width=0.9, alpha=0.5, color=palette, source=source, 
    #     legend_label=region)

    p.vbar(x='x', bottom=0, top='United States and Canada', 
        width=0.2, color='red', legend_label='US & CAN', source=source)

    p.vbar(x='x', bottom='United States and Canada', top='Latin America', 
        width=0.2, color='blue', legend_label='Latin Am', source=source)
    
    p.vbar(x='x', bottom='Latin America', top='Europe,  Middle East and Africa', 
        width=0.2, color='green', legend_label='EUR & ME', source=source)
    
    p.vbar(x='x', bottom='Europe,  Middle East and Africa', top='Asia-Pacific', 
        width=0.2, color='yellow', legend_label='APAC', source=source)


    p.y_range.start = 0
    p.y_range.end = 8000
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "vertical"

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
          
    factors, params_chart = transform_inputs(qtrs, years)
    print("factors:",factors, "params", params_chart)
    try:
        #when qtr, yr, AND area are selected
        params_chart[0][2]
        print('**************PRINT-TRY:REGION', params_chart[0][2])
        dict_ = chart1.get_area_y_ytd(params_chart, areas)
        p.x_range.factors = factors
        source.data = dict_
        print('=================TRY SOURCE UPDATED', source.data)
    except:
        print('=====EXCEPTION')
        # source.data = {
        #     'x': factors
        # }
        pass

    print('UPDATED SOURCE ALL DONE', source.data)



button_group_yr4.on_change("active",update_chart)
button_group_qtr4.on_change("active",update_chart)
button_group_area4.on_change("active",update_chart)



#for stacked charts, need to call all region for every x call or else the chart will break
factors = [('2', '2020', '')] 
b = ['United States and Canada', 'Latin America', 'Europe,  Middle East and Africa', 'Asia-Pacific']
chart1 = PeriodAmounts(dataframe)
dict_ = chart1.get_area_y_ytd(factors, b)

source = ColumnDataSource(data=dict_)

p = create_chart(factors, source, region, palette)

#annotations settings
# hover = HoverTool(tooltips=[
#     ('qtr,yr','@x'),
#     ('qytd revenue','$@y{0.1f} m'), 
#     ('subscribers','@y_subs{0.0 a}m')])
    
# p.add_tools(hover)

l = column(
    row(p), 
    row(Div(text="<h3>Quarter(s)</h3>"), button_group_qtr4),
    row(Div(text="<h3>Year(s)</h3>"), button_group_yr4),
    row(Div(text="<h3>Region(s)</h3>"), button_group_area4),
    )

tab_ytd_region_stacked = Panel(child=l, title="YTD Rev By Region")

tabs = Tabs(tabs=[ tab_ytd_region_stacked ])

curdoc().add_root(tabs)



