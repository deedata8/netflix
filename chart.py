from bokeh.models import FactorRange, ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import Range1d, LinearAxis, HoverTool, Tabs, Panel, Div
from bokeh.layouts import layout, column , row
from bokeh.io import curdoc, show
from df import groupings, dataframe
from classPeriodAmounts import PeriodAmounts
from widgets import button_group_area, button_group_period, button_group_qtr, button_group_yr, options_qtr, options_yr
from widgets import button_group_area2, button_group_period2, button_group_qtr2, button_group_yr2, options_qtr2, options_yr2


#list of params from widget inputs
def transform_inputs(qtrs_list, years_list, areas_list=[]):
    #create list of tuples with all selections
    params_chart = groupings(qtrs_list, years_list, areas_list)
    #convert all tuple values into strings in order to use in bokeh classification
    factors = [tuple(str(x) for x in tup) for tup in params_chart]
    return factors, params_chart


def create_chart(factors, source):

    p = figure(x_range=FactorRange(*factors), plot_height=350,
        toolbar_location=None, tools="")

    p.vbar(x='x', top='y', width=0.9, alpha=0.5, source=source)
    p.y_range.start = 0

    p.extra_y_ranges = {"Subscribers": Range1d(start=100, end=300)}
    p.triangle(x='x', y='y_subs', color="red", line_width=2, y_range_name="Subscribers", size=7, alpha=0.50, source=source)
    p.add_layout(LinearAxis(y_range_name="Subscribers"), 'right')

    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None

    return p


def update(attr, old ,new):
    qtrs = []
    years = []
    areas = []

    for i in button_group_qtr.active:
        qtrs.append(int(options_qtr[i]))

    for i in button_group_yr.active:
        years.append(int(options_yr[i]))
    
    for i in button_group_area.active:
        areas.append(int(options_yr[i]))
          
    factors, params_chart = transform_inputs(qtrs, years, areas)
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
    print('FACTORS:', factors)
    print('SOURCE:',source.data)



def update2(attr, old ,new):
    qtrs = []
    years = []
    areas = []

    for i in button_group_qtr2.active:
        qtrs.append(int(options_qtr[i]))

    for i in button_group_yr2.active:
        years.append(int(options_yr[i]))
    
    for i in button_group_area2.active:
        areas.append(int(options_yr[i]))
          
    factors, params_chart = transform_inputs(qtrs, years, areas)
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
    print('FACTORS:', factors)
    print('SOURCE:',source2.data)



button_group_yr.on_change("active",update)
button_group_qtr.on_change("active",update)
#button_group_area.on_change("active",update)
#button_group_period.on_change("active",update)



button_group_yr2.on_change("active",update2)
button_group_qtr2.on_change("active",update2)



#CREATE CHART FOR BY QTR AND BY YEAR
#starting params in chart
factors, params_chart = transform_inputs(['1','2','3','4'], ['2018','2019','2020'])
#instantiate for plotting data with df
chart1_data = PeriodAmounts(dataframe)
rev, subs = chart1_data.get_qtd(params_chart)
source = ColumnDataSource(data=dict(x=factors, y=rev, y_subs=subs))
p = create_chart(factors, source)
#annotations settings
hover = HoverTool(tooltips=[
    ('qtr,yr','@x'),
    ('revenue','$@y{0.1f} m'), 
    ('subscribers','@y_subs{0.0 a}m')])
p.add_tools(hover)
#first tab
l = column(
    row(p), 
    row(Div(text="<h3>Quarter(s)</h3>"), button_group_qtr),
    row(Div(text="<h3>Year(s)</h3>"), button_group_yr)
    )

tab = Panel(child=l, title="QTD Revenue")


#CREATE CHART FOR BY YTD AND BY YEAR
#starting params in chart
factors2, params_chart2 = transform_inputs(['1','2','3','4'], ['2018','2019','2020'])
print('===========PARAMS', params_chart2)
#instantiate for plotting data with df
chart2_data = PeriodAmounts(dataframe)
rev2, subs2 = chart2_data.get_ytd(params_chart2)
print('===========REV', rev2, '==================SUBS', subs2)
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
    row(Div(text="<h3>Quarter(s)</h3>"), button_group_qtr2),
    row(Div(text="<h3>Year(s)</h3>"), button_group_yr2)
    )
tab2 = Panel(child=l2, title="YTD Revenue")

# #filler plot
# p1 = figure(plot_width=300, plot_height=300)
# p1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
# tab1 = Panel(child=p1, title="circle")
#filler plot
p3 = figure(plot_width=300, plot_height=300)
p3.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)
tab3 = Panel(child=p3, title="line")


tabs = Tabs(tabs=[ tab, tab2, tab3 ])

curdoc().add_root(tabs)

