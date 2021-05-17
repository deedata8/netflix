from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, Div, Panel
from bokeh.layouts import column, row, layout
from widgets import button_group_qtr2, button_group_yr2, options_qtr2, options_yr2
from widgets import DEFAULT_YRS, DEFAULT_QTRS
from bar_chart import create_chart
from data import dataframe,  transform_inputs
from classPeriodAmounts import PeriodAmounts


def update(attr, old ,new):
    qtrs = []
    years = []

    for i in button_group_qtr2.active:
        qtrs.append(int(options_qtr2[i]))

    for i in button_group_yr2.active:
        years.append(int(options_yr2[i]))
          
    factors, params_chart = transform_inputs(qtrs, years)
    try:
        #when both qtr & yr are selected 
        params_chart[0][2]
        p.x_range.factors = factors
        y_rev, y_subs = chart_data.get_ytd(params_chart)
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


button_group_yr2.on_change("active",update)
button_group_qtr2.on_change("active",update)


#CREATE CHART FOR BY YTD AND BY YEAR
#starting params in chart
factors, params_chart = transform_inputs(DEFAULT_QTRS, DEFAULT_YRS)

#instantiate for plotting data with df
chart_data = PeriodAmounts(dataframe)
rev, subs = chart_data.get_ytd(params_chart)

source = ColumnDataSource(data=dict(x=factors, y=rev, y_subs=subs))

p = create_chart(factors, source, 'Netflix Revenue and Subscriber Count, YTD')

#annotations settings
hover2 = HoverTool(tooltips=[
    ('qtr,yr','@x'),
    ('ytd revenue','$@y{0.1f} m'), 
    ('subscribers','@y_subs{0.0 a}m')])
p.add_tools(hover2)

l = layout(children = [
    column(
        row(p),
        column(
            column(
                row(Div(text="<h3>Quarter</h3>")),
                row([button_group_qtr2]),
            ),
            column(
                row(Div(text="<h3>Year</h3>")),
                row([button_group_yr2]),
            ),
            sizing_mode = 'scale_width'
        ),
    )
], sizing_mode='scale_both')


tab_ytd = Panel(child=l, title="YTD Revenue")


