from __future__ import print_function
from bokeh.io import output_file
from bokeh.models import FactorRange, ColumnDataSource, CheckboxButtonGroup, RadioButtonGroup
from bokeh.plotting import figure, show
from bokeh.models import Range1d, LinearAxis, HoverTool, Tabs, Panel, Div
import numpy as np
import pandas as pd
from bokeh.layouts import layout, column , row
from bokeh.io import curdoc, show
import sys
from df import groupings, get_rev, get_subs

def transform_inputs(qtrs_list, years_list):
    data_chart = groupings(qtrs_list, years_list)
    factors = [tuple(str(x) for x in tup) for tup in data_chart]
    return factors, data_chart


def create_chart(factors, y_subs):
    p = figure(x_range=FactorRange(*factors), plot_height=350,
        toolbar_location=None, tools="")

    p.vbar(x='x', top='y', width=0.9, alpha=0.5, source=source)
    p.y_range.start = 0

    p.extra_y_ranges = {"Subscribers": Range1d(start=100, end=300)}
    p.triangle(x='x', y='y_subs', color="red", line_width=2, y_range_name="Subscribers", size=7, alpha=0.35, source=source)
    p.add_layout(LinearAxis(y_range_name="Subscribers"), 'right')

    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None

    return p

def update(attr, old ,new):
    qtrs = []
    years = []

    for i in button_group_qtr.active:
        qtrs.append(int(options_qtr[i]))

    for i in button_group_yr.active:
        years.append(int(options_yr[i]))

    factors, data_chart = transform_inputs(qtrs, years)
    y = get_rev(data_chart)
    y_subs = get_subs(data_chart)
    source.data = {
        'x': factors,
        'y': y,
        'y_subs': y_subs
    }
    #print(source.data)



options_yr=['2018', '2019', '2020']
button_group_yr=CheckboxButtonGroup(labels=options_yr)
button_group_yr.on_change("active",update)

options_qtr=['1', '2', '3', '4']
button_group_qtr=CheckboxButtonGroup(labels=options_qtr)
button_group_qtr.on_change("active",update)

factors, data_chart = transform_inputs(options_qtr, options_yr)
y_rev = get_rev(data_chart)
y_subs = get_subs(data_chart)
source = ColumnDataSource(data=dict(x=factors, y=y_rev, y_subs=y_subs))
p = create_chart(factors, y_subs)

hover = HoverTool(tooltips=[
    ('qtr,yr','@x'),
    ('revenue','$@y{0.1f} m'), 
    ('subscribers','@y_subs{0.0 a}m')])
p.add_tools(hover)

p1 = figure(plot_width=300, plot_height=300)
p1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
tab1 = Panel(child=p1, title="circle")

p2 = figure(plot_width=300, plot_height=300)
p2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)
tab2 = Panel(child=p2, title="line")

# l = layout([
#     [p],
#     [button_group_qtr],
#     [button_group_yr] 
# ])
l = column(
    row(p), 
    row(Div(text="<h3>Quarter(s)</h3>"), button_group_qtr),
    row(Div(text="<h3>Year(s)</h3>"), button_group_yr)
    )

tab = Panel(child=l, title="Revenue")

tabs = Tabs(tabs=[ tab, tab1, tab2 ])

# lay_out = layout([
#     tab 
# ])

# curdoc().add_root(lay_out)



curdoc().add_root(tabs)