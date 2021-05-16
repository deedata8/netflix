from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, Div, Panel
from bokeh.layouts import layout, column, row
from data import groupings, dataframe,  transform_inputs
from classPeriodAmounts import PeriodAmounts
from widgets import button_group_qtr2, button_group_yr2, options_qtr2, options_yr2
from bar_chart import create_chart


def update2(attr, old ,new):
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
        p2.x_range.factors = factors
        y_rev, y_subs = chart2_data.get_ytd(params_chart)
        source2.data = {
            'x': factors,
            'y': y_rev,
            'y_subs': y_subs
        }
    except:
        source2.data = {
            'x': [],
            'y': [],
            'y_subs': []
        }
        #p.x_range.factors = []


button_group_yr2.on_change("active",update2)
button_group_qtr2.on_change("active",update2)


#CREATE CHART FOR BY YTD AND BY YEAR
#starting params in chart
factors2, params_chart2 = transform_inputs(['1','2','3','4'], ['2018','2019','2020'])

#instantiate for plotting data with df
chart2_data = PeriodAmounts(dataframe)
rev2, subs2 = chart2_data.get_ytd(params_chart2)

source2 = ColumnDataSource(data=dict(x=factors2, y=rev2, y_subs=subs2))

p2 = create_chart(factors2, source2)
#annotations settings
hover2 = HoverTool(tooltips=[
    ('qtr,yr','@x'),
    ('ytd revenue','$@y{0.1f} m'), 
    ('subscribers','@y_subs{0.0 a}m')])
p2.add_tools(hover2)
#second tab
l2 = column(
    row(p2), 
    row(Div(text="<h3>Quarter</h3>"), button_group_qtr2),
    row(Div(text="<h3>Year</h3>"), button_group_yr2)
    )
tab_ytd = Panel(child=l2, title="YTD Revenue")


