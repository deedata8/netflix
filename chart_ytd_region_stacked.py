from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import GlyphRenderer, HoverTool, FactorRange, Legend
from bokeh.models import HoverTool, Div, Panel
from bokeh.layouts import layout, column, row
from data import groupings, dataframe,  transform_inputs
from classPeriodAmounts import PeriodAmounts
from widgets import button_group_area5, button_group_qtr5, button_group_yr5, options_qtr5, options_yr5, options_area5
from bokeh.models import Tabs  
import bokeh.plotting
import bokeh.layouts


COLORS_REGION = {
    'United States and Canada': "blue", 
    'Latin America': "red",   
    'Europe,  Middle East and Africa': "green",   
    'Asia-Pacific': "yellow"
    }


#intial data: first data point as zeroes because cannot remove first glyph- perhaps a bug (each region presented is a glyph)
region = ['', 'United States and Canada', 'Latin America', 'Europe,  Middle East and Africa', 'Asia-Pacific']
color = ['','blue','red', 'green', 'yellow']
factors, params_chart = transform_inputs(['1'], ['2018'])
chart1 = PeriodAmounts(dataframe)
data = {'x' : factors,
    '' : chart1.get_area_specific_ytd(factors, ''), 
    'United States and Canada' : chart1.get_area_specific_ytd(factors, 'United States and Canada'), 
    'Latin America' : chart1.get_area_specific_ytd(factors, 'Latin America'), 
    'Europe,  Middle East and Africa' : chart1.get_area_specific_ytd(factors, 'Europe,  Middle East and Africa'),   
    'Asia-Pacific' : chart1.get_area_specific_ytd(factors, 'Asia-Pacific')  
    }

#figure set
p = figure(x_range=FactorRange(*factors), plot_height=350, plot_width=1000, 
        title="Revenue Year-to-date",
        toolbar_location=None, tools="hover", 
        tooltips="$name @x: @$name")

#starting glyphs
p.vbar_stack(region, x='x', width=0.9, color=color, source=data,
            legend_label = region)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.add_layout(p.legend[0], 'right')

def update_chart(attr, old, new):

    qtrs = []
    years = []
    areas = []

    #reset glyphs by removing them in order to regenerate
    for i in range(len(p.renderers), 1, -1):
        if type(p.renderers[i-1]) == GlyphRenderer:
            print('GLYPH_OLD_INNER')
            p.renderers.pop(i-1)
        elif type(p.renderers[i-1]) == Legend:
            print('LEGEND_OLD')
            p.renderers.pop(i-1)
        print('END CYCLE')

    for i in button_group_qtr5.active:
        qtrs.append(int(options_qtr5[i]))

    for i in button_group_yr5.active:
        years.append(int(options_yr5[i]))
    
    for i in button_group_area5.active:
        areas.append(options_area5[i])

    factors, params_chart = transform_inputs(qtrs, years)
    chart1 = PeriodAmounts(dataframe)
    #dict_ only being used for IF condition
    dict_ = chart1.get_area_y_ytd1(params_chart, areas)

    try:
        #if an area selected or change in regions selection --> trigger update/regen chart
        if len(dict_) > 1:

            colors_updated = []
            for i in dict_:
                if i == "x":
                    pass
                else:
                    colors_updated.append(COLORS_REGION[i])
            
            dict1 = {key: value for key, value in dict_.items() if key != "x"}
            regions_updated = list(dict1.keys())

            #appears need to be in this format and update by key for the chart to regenerate
            #returns for all regions based on period, filter is by "regions_updated" param
            data_updated = {'x' : factors,
                'United States and Canada' : chart1.get_area_specific_ytd(factors, 'United States and Canada'), 
                'Latin America' : chart1.get_area_specific_ytd(factors, 'Latin America'),   
                'Europe,  Middle East and Africa' : chart1.get_area_specific_ytd(factors, 'Europe,  Middle East and Africa'),   
                'Asia-Pacific' : chart1.get_area_specific_ytd(factors, 'Asia-Pacific')
                }
        
            p.vbar_stack(regions_updated , x='x', width=0.9, color=colors_updated, 
                        source=data_updated,
                        legend_label=regions_updated )
            
            p.x_range.factors=factors
            p.add_tools(HoverTool(tooltips="$name- YTD:@x @$name{$0.1f} m"))
         
        else:
            #print('NO UPDATE', params_chart[0][2])
            pass
    except:
        #print('+++++++++++++++++++DOES NOT EXIST params_chart[0][2]')
        pass


button_group_yr5.on_change("active",update_chart)
button_group_qtr5.on_change("active",update_chart)
button_group_area5.on_change("active",update_chart)




# curdoc().add_root(
#     column(
#     row(button_group_yr5),
#     row(button_group_qtr5),
#     row(button_group_area5),
#     row(p))
#     )



l = column(
    row(p), 
    row(Div(text="<h3>Quarter</h3>"), button_group_qtr5),
    row(Div(text="<h3>Year</h3>"), button_group_yr5),
    row(Div(text="<h3>Region</h3>"), button_group_area5)
    )

#c = column(children = [p, l], sizing_mode = 'stretch_both')
#curdoc().add_root(c)


tab_ytd_stacked = Panel(child=l, title="YTD Rev By Region Stacked")
