from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, Div, Panel
from bokeh.layouts import column, row, layout

from widgets import button_group_area3, button_group_qtr3, button_group_yr3, options_qtr3, options_yr3, options_area3
from widgets import DEFAULT_YRS, DEFAULT_QTRS, DEFAULT_AREAS
from bar_chart import create_chart_region
from widgets import REGION_PALLETE
from data import dataframe,  transform_inputs
from classPeriodAmounts import PeriodAmounts



def update_chart(attr, old ,new):
    qtrs = []
    years = []
    areas = []

    for i in button_group_qtr3.active:
        qtrs.append(int(options_qtr3[i]))

    for i in button_group_yr3.active:
        years.append(int(options_yr3[i]))
    
    for i in button_group_area3.active:
        areas.append(options_area3[i])
          
    factors, params_chart = transform_inputs(qtrs, years, areas)

    try:
        #when qtr, yr, AND area are selected 
        params_chart[0][2]
        p.x_range.factors = factors
        y_rev, y_subs = chart1_data.get_qtd(params_chart)
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


button_group_yr3.on_change("active",update_chart)
button_group_qtr3.on_change("active",update_chart)
button_group_area3.on_change("active",update_chart)


#CREATE CHART FOR BY QTR AND BY YEAR
#starting params in chart
factors, params_chart = transform_inputs(DEFAULT_QTRS, DEFAULT_YRS, DEFAULT_AREAS)
#instantiate for plotting data with df
chart1_data = PeriodAmounts(dataframe)
rev, subs = chart1_data.get_qtd(params_chart)
source = ColumnDataSource(data=dict(x=factors, y=rev, y_subs=subs))
p = create_chart_region(factors, source, options_area3, REGION_PALLETE)
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
                row([button_group_qtr3])
            ),
            column(
                row(Div(text="<h3>Year</h3>")),
                row([button_group_yr3])
            ),
            column(
                row(Div(text="<h3>Area</h3>")),
                row([button_group_area3])
            ), 
            sizing_mode = 'scale_width'
        )
    )
], sizing_mode='scale_both')


tab_qtd_region = Panel(child=l, title="QTD Rev By Region")



