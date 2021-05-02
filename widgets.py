import panel as pn
import param

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, FactorRange

pn.extension()


checkbutton_qtrs = pn.widgets.CheckButtonGroup(name='Select Quarter(s)', options=[1,2,3,4])
radio_period = pn.widgets.RadioBoxGroup(name='RadioBoxGroup1', options=['QTD', 'YTD'], inline=True)
checkbutton_yrs= pn.widgets.CheckButtonGroup(name='Select Years(s)', options=[2018,2019,2020])

radio_period

checkbutton_qtrs

checkbutton_qtrs