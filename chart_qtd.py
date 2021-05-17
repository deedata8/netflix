from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, Div, Panel
from bokeh.layouts import column , row, layout
from widgets import button_group_qtr, button_group_yr, options_qtr, options_yr
from widgets import DEFAULT_YRS, DEFAULT_QTRS
from bar_chart import create_chart
from data import dataframe,  transform_inputs
from classPeriodAmounts import PeriodAmounts


def update_chart(attr, old ,new):
    qtrs = []
    years = []

    for i in button_group_qtr.active:
        qtrs.append(int(options_qtr[i]))

    for i in button_group_yr.active:
        years.append(int(options_yr[i]))
          
    factors, params_chart = transform_inputs(qtrs, years)
    try:
        #when both qtr & yr are selected 
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
        #p.x_range.factors = []



button_group_yr.on_change("active",update_chart)
button_group_qtr.on_change("active",update_chart)

#CREATE CHART FOR BY QTR AND BY YEAR
#starting params in chart
factors, params_chart = transform_inputs(DEFAULT_QTRS, DEFAULT_YRS)
#instantiate for plotting data with df
chart1_data = PeriodAmounts(dataframe)
rev, subs = chart1_data.get_qtd(params_chart)
source = ColumnDataSource(data=dict(x=factors, y=rev, y_subs=subs))
p = create_chart(factors, source, 'Netflix Revenue and Subscriber Count, QTD')
#annotations settings
hover = HoverTool(tooltips=[
    ('qtr,yr','@x'),
    ('revenue','$@y{0.1f} m'), 
    ('subscribers','@y_subs{0.0 a}m')])
p.add_tools(hover)


l = layout(children = [
    column(
        row(p),
        column(
            column(
                row(Div(text="<h3>Quarter</h3>")),
                row([button_group_qtr]),
            ),
            column(
                row(Div(text="<h3>Year</h3>")),
                row([button_group_yr]),
            ),
            sizing_mode = 'scale_width'
        ),
    )
], sizing_mode='scale_both')


tab_qtd = Panel(child=l, title="QTD Revenue")

