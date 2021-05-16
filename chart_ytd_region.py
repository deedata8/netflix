from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, Div, Panel
from bokeh.layouts import column, row, layout
from widgets import button_group_area4, button_group_qtr4, button_group_yr4, options_qtr4, options_yr4, options_area4
from bar_chart import create_chart_region
from classPeriodAmounts import PeriodAmounts
from widgets import REGION_PALLETE, DEFAULT_YRS, DEFAULT_QTRS, DEFAULT_AREAS
from data import dataframe, transform_inputs



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

button_group_yr4.on_change("active",update_chart)
button_group_qtr4.on_change("active",update_chart)
button_group_area4.on_change("active",update_chart)

#CREATE CHART FOR BY QTR AND BY YEAR
#starting params in chart, widgets only takes a list of strings
factors, params_chart = transform_inputs(DEFAULT_QTRS, DEFAULT_YRS, DEFAULT_AREAS)

#instantiate for plotting data with df
chart1_data = PeriodAmounts(dataframe)
rev, subs = chart1_data.get_ytd(params_chart)

source = ColumnDataSource(data=dict(x=factors, y=rev, y_subs=subs))
p = create_chart_region(factors, source, options_area4, REGION_PALLETE)
#annotations settings
hover = HoverTool(tooltips=[
    #('qtr,yr','@x'),
    ('qtd revenue','$@y{0.1f} m'), 
    ('subscribers','@y_subs{0.0 a}m')])
p.add_tools(hover)

l = layout(children = [
    column(
        row(
            column(p,
                sizing_mode='scale_both'
            )
        ),
        row(
            column(
                Div(text="<h3></h3>"),
                sizing_mode='scale_both'
            )
        ),
        row(
            column(
                row(Div(text="<h3>Quarter</h3>")),
                row([button_group_qtr4])
            ),
            column(
                row(Div(text="<h3>Year</h3>")),
                row([button_group_yr4])
            ),
            column(
                row(Div(text="<h3>Area</h3>")),
                row([button_group_area4])
            ), 
            sizing_mode = 'scale_width'
        )
    )
], sizing_mode='scale_both')

tab_ytd_region = Panel(child=l, title="YTD Rev By Region")




