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



#qtr, year
fruits = [('1', '2018',''), ('2', '2018','')]
#region
years = ['United States and Canada', 'Latin America']
colors1 = ["blue", "red", "yellow", "green"]
colors = ["blue", "red"]

data = {'fruits' : fruits,
        'United States and Canada' : [2000, 1000],
        'Latin America' : [5000, 3000]}


#figure set
p = figure(x_range=FactorRange(*fruits), plot_height=250, #plot_width=100, 
           title="Fruit Counts by Year",
           toolbar_location=None, tools="hover", 
           tooltips="$name @fruits: @$name")

#starting glyphs
p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=data,
             legend=[value(x) for x in years])

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
    print("===========factors:",factors, "================params", params_chart)
    chart1 = PeriodAmounts(dataframe)
    dict_ = chart1.get_area_y_ytd1(params_chart, areas)
    print("DICTIONARY FOR DATA------------------", dict_)

    try:
        if len(dict_) > 1:

            my_palette_updated=len(areas)
            colors_updated = colors1[:my_palette_updated]

            fruits_updated = factors

            dict1 = {key: value for key, value in dict_.items() if key != "x"}
            years_updated = list(dict1.keys())

            #appears need to be in this format and update by key for the chart to regenerate
            data_updated = {'x' : fruits_updated,
                'United States and Canada' : chart1.get_area_specific_ytd(fruits_updated, 'United States and Canada'), 
                'Latin America' : chart1.get_area_specific_ytd(fruits_updated, 'Latin America'),   
                'Europe,  Middle East and Africa' : chart1.get_area_specific_ytd(fruits_updated, 'Europe,  Middle East and Africa'),   
                'Asia-Pacific' : chart1.get_area_specific_ytd(fruits_updated, 'Asia-Pacific')
                }

            #reset glyphs by removing them
            for i in range(len(p.renderers), 1, -1):
                if type(p.renderers[i-1]) == GlyphRenderer:
                    print("glyph")
                    p.renderers.pop(i-1)
                elif type(p.renderers[i-1]) == Legend:
                    print("legend")
                    p.renderers.pop(i-1)
        
            p.vbar_stack(years_updated, x='x', width=0.9, color=colors_updated, 
                        source=data_updated,
                        legend=[value(x) for x in years_updated])
            
            p.x_range.factors=fruits_updated
            p.y_range.start = 0
            p.x_range.range_padding = 0.1
            p.xgrid.grid_line_color = None
            p.axis.minor_tick_line_color = None
            p.outline_line_color = None
            p.legend.location = "top_left"
            p.legend.orientation = "horizontal"
            #p.add_tools(HoverTool(tooltips="$name @fruits: @$name"))

        else:
            print('+++++++++++++++++++DOES NOT UPDATE', params_chart[0][2])
    except:
        print('+++++++++++++++++++DOES NOT EXIST params_chart[0][2]')
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