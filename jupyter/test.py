from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.transform import dodge, stack
from bokeh.driving import bounce
import numpy as np
import pandas as pd

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums']

years = ['2013', '2014', '2015', '2016', '2017', '2018']

colors = ['#c9d9d3', '#718dbf', '#e84d60', '#b84d67', '#776dbd']


data = {'years'      : years,
        'Apples'     : [2, 1, 4, 3, 2, 1],
        'Pears'      : [3, 2, 4, 4, 5, 1],
        'Nectarines' : [5, 4, 2, 1, 3, 1],
        'Plums'      : [2, 2, 2, 5, 3, 1]}


source = ColumnDataSource(data=data)


#figure for stacked bars
stack_fig = figure(x_range=years, plot_height=250, title="Stacked Fruit Counts by Year",
           toolbar_location=None, tools="")

#settings to simulate my setup
width_group = 0.8
gap = 0.02

#here I am calculating teh dodges/bar widths automatically
width_bar= round((width_group-((len(fruits)-1)*gap))/len(fruits), 3)
# dodges = np.linspace(-0.5*(len(fruits)*width_bar+((len(fruits)-1)*gap))+(width_bar*.5),
#                          0.5*(len(fruits)*width_bar+((len(fruits)-1)*gap))-(width_bar*.5),
#                          len(fruits))



#loop that creates stacked vbars. I could not get vbar_stack to work in my other code. 
bottom_fields = []
top_fields = []
for bar, fruit in enumerate(fruits):
    top_fields.append(fruit)
    stack_fig.vbar(bottom=stack(*bottom_fields),
                   top=stack(*top_fields),
                   x='years',
                   width=width_group,
                   source=source,
                   color=colors[bar])
    bottom_fields.append(fruit)

#set up layout
#column = column([stack_fig])


# #bounce wrapper to index columns
# @bounce([1, 2, 3, 4])
def get_update(attr, old, new):
    
    source.data = {
        'years'      : years,
        'Apples'     : [20, 10, 40, 30, 20, 10],
        'Pears'      : [3, 2, 4, 4, 5, 1],
        'Nectarines' : [5, 4, 2, 1, 3, 1],
        'Plums'      : [2, 2, 2, 5, 3, 1]
        }



from bokeh.models import CheckboxButtonGroup

#chart qtd
options_yr=['50']
button_group=CheckboxButtonGroup(labels=options_yr)

button_group.on_change("active",get_update)

l = column(
    row(stack_fig),
    row(button_group),
    )

# tab_ytd_region_stacked = Panel(child=l, title="YTD Rev By Region")

# tabs = Tabs(tabs=[ tab_ytd_region_stacked ])

curdoc().add_root(l)

# curdoc().add_periodic_callback(get_update, 5000)
# curdoc().add_root(column)