from bokeh.core.properties import value
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models.widgets import Button
from bokeh.palettes import Category20b,Category20c
import random
from bokeh.layouts import row
from bokeh.models import GlyphRenderer,Legend, HoverTool


from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, Div, Panel
from bokeh.layouts import layout, column, row
from data import groupings, dataframe,  transform_inputs
from classPeriodAmounts import PeriodAmounts
from widgets import button_group_area5, button_group_qtr5, button_group_yr5, options_qtr5, options_yr5, options_area5
from bokeh.transform import factor_cmap
from bokeh.core.properties import value
#from bar_chart import create_chart

from bokeh.io import curdoc
from bokeh.models import Tabs
from bokeh.models import FactorRange, GlyphRenderer, Legend, HoverTool  
from bokeh.plotting import figure
from bokeh.models import Range1d, LinearAxis, VBar


colors_region = {
    'United States and Canada': "blue", 
    'Latin America': "red",   
    'Europe,  Middle East and Africa': "green",   
    'Asia-Pacific': "yellow"
    }

#qtr, year
period = [('1', '2018',''), ('2', '2018','')]
region = ['United States and Canada', 'Latin America', 'Europe,  Middle East and Africa','Asia-Pacific']
colors = ["blue", "red", "green", "yellow"]

data = {'x' : period,
        'United States and Canada' : [2000, 1000],
        'Latin America' : [5000, 3000],
        'Europe,  Middle East and Africa': [6000, 3000],
        'Asia-Pacific': [4000, 4000]
        }

#figure set
p = figure(x_range=FactorRange(*period), plot_height=250, #plot_width=100, 
           title="Revenue Year-to-date",
           toolbar_location=None, tools="hover", 
           tooltips="$name @fruits: @$name")

#starting glyphs
p.vbar_stack(region, x='x', width=0.9, color=colors, source=data,
            legend_label = region)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"


def update_chart(attr, old, new):

    qtrs = []
    years = []
    areas = []

    for i in button_group_qtr5.active:
        qtrs.append(int(options_qtr5[i]))

    for i in button_group_yr5.active:
        years.append(int(options_yr5[i]))
    
    for i in button_group_area5.active:
        areas.append(options_area5[i])

    factors, params_chart = transform_inputs(qtrs, years)
    chart1 = PeriodAmounts(dataframe)
    dict_ = chart1.get_area_y_ytd1(params_chart, areas)

    try:
        #if an area selected or change in regions selection --> trigger update/regen chart
        if len(dict_) > 1:

            colors_updated = []
            for i in dict_:
                if i == "x":
                    pass
                else:
                    colors_updated.append(colors_region[i])

            dict1 = {key: value for key, value in dict_.items() if key != "x"}
            regions_updated = list(dict1.keys())

            #appears need to be in this format and update by key for the chart to regenerate
            data_updated = {'x' : factors,
                'United States and Canada' : chart1.get_area_specific_ytd(factors, 'United States and Canada'), 
                'Latin America' : chart1.get_area_specific_ytd(factors, 'Latin America'),   
                'Europe,  Middle East and Africa' : chart1.get_area_specific_ytd(factors, 'Europe,  Middle East and Africa'),   
                'Asia-Pacific' : chart1.get_area_specific_ytd(factors, 'Asia-Pacific')
                }

            #reset glyphs by removing them
            for i in range(len(p.renderers), 1, -1):
                if type(p.renderers[i-1]) == GlyphRenderer:
                    p.renderers.pop(i-1)
                elif type(p.renderers[i-1]) == Legend:
                    p.renderers.pop(i-1)
        
            p.vbar_stack(regions_updated, x='x', width=0.9, color=colors_updated, 
                        source=data_updated,
                        legend_label = regions_updated)
            
            p.x_range.factors=factors
            p.y_range.start = 0
            p.x_range.range_padding = 0.1
            p.xgrid.grid_line_color = None
            p.axis.minor_tick_line_color = None
            p.outline_line_color = None
            p.legend.location = "top_left"
            p.legend.orientation = "horizontal"
            p.add_tools(HoverTool(tooltips="$name @fruits: @$name"))

        else:
            #print('NO UPDATE', params_chart[0][2])
            pass
    except:
        #print('+++++++++++++++++++DOES NOT EXIST params_chart[0][2]')
        pass


button_group_yr5.on_change("active",update_chart)
button_group_qtr5.on_change("active",update_chart)
button_group_area5.on_change("active",update_chart)



curdoc().add_root(
    column(
    row(button_group_yr5),
    row(button_group_qtr5),
    row(button_group_area5),
    row(p))
    )