from bokeh.plotting import figure
from bokeh.layouts import row
from bokeh.models import GlyphRenderer, HoverTool, FactorRange, Legend
from bokeh.models import HoverTool, Div, Panel
from bokeh.layouts import column, row, layout
from widgets import button_group_area5, button_group_qtr5, button_group_yr5, options_qtr5, options_yr5, options_area5
from widgets import DEFAULT_YRS, DEFAULT_QTRS
from data import dataframe,  transform_inputs
from classPeriodAmounts import PeriodAmounts
from widgets import COLORS_REGION


#intial data: first data point as zeroes because cannot remove first glyph- perhaps a bug (each region presented is a glyph)
region = ['', 'United States and Canada', 'Latin America', 'Europe,  Middle East and Africa', 'Asia-Pacific']
color = ['','#6baed6','#fd8d3c', '#74c476', '#9e9ac8']
factors, params_chart = transform_inputs(DEFAULT_QTRS, DEFAULT_YRS)
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
            p.renderers.pop(i-1)
        elif type(p.renderers[i-1]) == Legend:
            p.renderers.pop(i-1)

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
            pass
    except:
        pass


button_group_yr5.on_change("active",update_chart)
button_group_qtr5.on_change("active",update_chart)
button_group_area5.on_change("active",update_chart)


l = layout(children = [
    column(
        row(p),
        column(
            column(
                row(Div(text="<h3>Quarter</h3>")),
                row([button_group_qtr5]),
            ),
            column(
                row(Div(text="<h3>Year</h3>")),
                row([button_group_yr5]),
            ),
                column(
                row(Div(text="<h3>Region</h3>")),
                row([button_group_area5]),
            ),
            sizing_mode = 'scale_width'
        ),
    )
], sizing_mode='scale_both')

tab_ytd_stacked = Panel(child=l, title="YTD Rev By Region Stacked")
