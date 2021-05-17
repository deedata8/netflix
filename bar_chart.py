from bokeh.models import FactorRange #requires list of string tuples 
from bokeh.plotting import figure
from bokeh.models import Range1d, LinearAxis
from bokeh.transform import factor_cmap


def create_chart(factors, source, title):

    p = figure(x_range=FactorRange(*factors), plot_height=350, plot_width=1000, title=title,
        toolbar_location=None, tools="")

    p.vbar(x='x', top='y', width=0.9, alpha=0.5, source=source)
    p.y_range.start = 0

    p.extra_y_ranges = {"Subscribers": Range1d(start=100, end=300)}
    p.triangle(x='x', y='y_subs', color="red", line_width=2, y_range_name="Subscribers", size=7, alpha=0.50, source=source)
    p.add_layout(LinearAxis(y_range_name="Subscribers"), 'right')

    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None

    return p


#grouped bar charts with assigned colors
def create_chart_region(factors, source, color_factors, palette, title):

    p = figure(x_range=FactorRange(*factors), plot_height=350, plot_width=1000, title=title,
        toolbar_location=None, tools="")

    p.vbar(x='x', top='y', width=0.9, alpha=0.5, source=source,
        fill_color=factor_cmap('x', palette=palette, factors=color_factors, start=2, end=3))
    
    p.y_range.start = 0

    p.extra_y_ranges = {"Subscribers": Range1d(start=0, end=100)}
    p.triangle(x='x', y='y_subs', color="red", line_width=2, y_range_name="Subscribers", size=7, alpha=0.50, source=source)
    p.add_layout(LinearAxis(y_range_name="Subscribers"), 'right')

    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 0.95 
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None

    return p



