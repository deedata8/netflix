from __future__ import print_function
from bokeh.io import output_file
from bokeh.models import FactorRange, ColumnDataSource, CheckboxButtonGroup, RadioButtonGroup
from bokeh.plotting import figure, show
from bokeh.models import Range1d, LinearAxis
import panel as pn
import param
import numpy as np
import pandas as pd
from bokeh.layouts import layout
from bokeh.io import curdoc, show
import logging
import sys
from df import groupings, get_vals, get_subs


qtrs_ = [1,2,3,4]
yrs_ = [2018,2019,2020]


#pn.extension()
logger = logging.getLogger()

def transform_inputs(years_list):
    data_chart = groupings(qtrs_, years_list)
    factors = [tuple(str(x) for x in tup) for tup in data_chart]
    return factors, data_chart



#def transform_inputs(year):
    #inputs
data_chart = groupings(qtrs_, yrs_)
    #data_chart = groupings(checkbutton_qtrs.value, checkbox_button_group.value)
    #convert int tuples to strings in order to use FactorRange (multi-x-axis type)
factors = [tuple(str(x) for x in tup) for tup in data_chart]
    #return factors, data_chart

    #factors, data_chart = transform_inputs()

    #get info from df 
y = get_vals(data_chart)

#use CDS for interactive wdigets
source = ColumnDataSource(data=dict(x=factors, y=y))

p = figure(x_range=FactorRange(*factors), plot_height=350,
       toolbar_location=None, tools="")

p.vbar(x='x', top='y', width=0.9, alpha=0.5, source=source)
p.y_range.start = 0

p.extra_y_ranges = {"Subscribers": Range1d(start=100, end=300)}
p.triangle(x=factors, y=get_subs(data_chart), color="red", line_width=2, y_range_name="Subscribers", size=7, alpha=0.35)
p.add_layout(LinearAxis(y_range_name="Subscribers"), 'right')

p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None

def update1(attr, old, new):
    #can only work for one year-- need to implement widget that returns list of years and qtrs
    #to update subsscriber data as well
    year = int(options[radio.active])
    years = []
    years.append(year) 
    factors, data_chart = transform_inputs(years)
    y = get_vals(data_chart)
    source.data = {
        'x': factors,
        'y': y
    }


options=['2018', '2019', '2020']
radio=RadioButtonGroup(labels=options)
radio.on_change("active",update1)

#to render widgets in page
lay_out = layout([
    p,
    radio
])

curdoc().add_root(lay_out)