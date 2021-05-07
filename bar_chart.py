from bokeh.models import FactorRange #requires list of string tuples 
from bokeh.plotting import figure
from bokeh.models import Range1d, LinearAxis


def create_chart(factors, source):

    p = figure(x_range=FactorRange(*factors), plot_height=350,
        toolbar_location=None, tools="")

    p.vbar(x='x', top='y', width=0.9, alpha=0.5, source=source)
    p.y_range.start = 0

    p.extra_y_ranges = {"Subscribers": Range1d(start=100, end=300)}
    p.triangle(x='x', y='y_subs', color="red", line_width=2, y_range_name="Subscribers", size=7, alpha=0.50, source=source)
    p.add_layout(LinearAxis(y_range_name="Subscribers"), 'right')

    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None

    return p