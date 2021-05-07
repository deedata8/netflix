from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure, curdoc

from bokeh.transform import factor_cmap

x = [('1', '2018', 'US'),('2', '2018', 'Asia'),('1', '2019', 'US'),('2', '2019', 'Asia')]
#x = [('1','US'),('2', 'Asia'),('3','US'),('4','Asia')]

data = {
'x': [('1', '2018', 'US'),('2', '2018', 'Asia'),('1', '2019', 'US'),('2', '2019', 'Asia')],
'y': [2,3,3,2],
}

# data = {
# 'x': [('1','US'),('2', 'Asia'),('3','US'),('4','Asia')],
# 'y': [2,3,3,2],
# }


source1 = ColumnDataSource(data=data)
source1.data

palette = ["red", "blue"]

regions = ['US', 'Asia']

p = figure(x_range=FactorRange(*x), plot_height=350, title="Fruit Counts by Year",
           toolbar_location=None, tools="")

p.vbar(x='x', top='y', width=0.9, source=source1, line_color="white",
       #start color based on start position 1 and end position 2
       fill_color=factor_cmap('x', palette=palette, factors=regions, start=2, end=3))

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None



curdoc().add_root(p)