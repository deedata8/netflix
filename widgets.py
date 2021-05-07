from bokeh.models import CheckboxButtonGroup

options_yr=['2018', '2019', '2020']
button_group_yr=CheckboxButtonGroup(labels=options_yr)

options_qtr=['1', '2', '3', '4']
button_group_qtr=CheckboxButtonGroup(labels=options_qtr)

options_area=['United States and Canada', 'Latin America', 'Europe,  Middle East and Africa', 'Asia-Pacific']
button_group_area=CheckboxButtonGroup(labels=options_area)

options_period=['QTD', 'YTD']
button_group_period=CheckboxButtonGroup(labels=options_period)