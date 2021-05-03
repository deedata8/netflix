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
from df import groupings, get_rev, get_subs

#data range inputs for initial generation of chart
qtrs_ = [1,2,3,4]
yrs_ = [2018,2019,2020]

#logger = logging.getLogger()
#logger.warning("THIS IS A WARNING MESSAGE")

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
    #can only work for one year-- need to implement widget that returns list of years and qtrs
    year = int(options[radio.active])
    years = []
    years.append(year) 
    #qtrs_ a global var
    factors, data_chart = transform_inputs(qtrs_, years)
    y = get_rev(data_chart)
    y_subs = get_subs(data_chart)
    source.data = {
        'x': factors,
        'y': y,
        'y_subs': y_subs
    }

factors, data_chart = transform_inputs(qtrs_,yrs_)
y_rev = get_rev(data_chart)
y_subs = get_subs(data_chart)
source = ColumnDataSource(data=dict(x=factors, y=y_rev, y_subs=y_subs))
p = create_chart(factors, y_subs)

options=['2018', '2019', '2020']
radio=RadioButtonGroup(labels=options)
radio.on_change("active",update)

#to render widgets in page
lay_out = layout([
    p,
    radio
])

curdoc().add_root(lay_out)