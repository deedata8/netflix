from os.path import dirname, join
import pandas as pd
import collections
from bokeh.io import curdoc
from bokeh.layouts import column, row, layout
from bokeh.models import (Button, ColumnDataSource, CustomJS, DataTable,
                          NumberFormatter, TableColumn, Div, Panel)
    

df = pd.read_csv(join(dirname(__file__), '../data/Netflix.csv'))

#to keep dict order
source = ColumnDataSource(data=collections.OrderedDict())
source.data = {
    'Region'          : df['Area'],
    'QTR-YR'         : df['Years'],
    'Revenue'      : df[' Revenue '].str.replace(',', '').astype(float),
    'Subscribers'   : df[' Subscribers '].str.replace(',', '').astype(float)
}

columns = [
    TableColumn(field='Region', title='Region'),
    TableColumn(field='QTR-YR', title='QTR-YR'),
    TableColumn(field='Subscribers', title='Subscribers', formatter=NumberFormatter(format='0,0')),
    TableColumn(field='Revenue', title='Revenue', formatter=NumberFormatter(format='$0,0')),
]

columnNames = [x.field for x in columns]

#create bokeh datatable from CDS
data_table = DataTable(source=source, columns=columns, width=800)
button = Button(label='Download Data', button_type='success')
button.js_on_click(CustomJS(args={'source': source, 'columns': columnNames},
                            code=open(join(dirname(__file__), "download.js")).read()))

controls = column(button)

# curdoc().add_root(row(controls, data_table))
# curdoc().title = "Export CSV"


l = layout(children = [
    column(
        column(
            column(
                row(Div(text="<h3>Download data used in Netflix Dashboard:</h3>")),
                row([button]),
            ),
            column(
                row(Div(text="<a href='https://www.kaggle.com/pariaagharabi/netflix2020'>Original Kaggle Netflix Data Set</a>")),
            ),
            column(
                row(Div(text="<a href='https://github.com/deedata8/netflix'>GitHub Source Code</a>")),
            ),
            column(
                row(Div(text="<h3></h3>")),
                row([data_table]),
            ),
        ),
    )
], sizing_mode='scale_both')


csv_dl = Panel(child=l, title="Data Source")

