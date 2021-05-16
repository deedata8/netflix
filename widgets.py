from bokeh.models import CheckboxButtonGroup


#REGION_PALLETE = ["blue", "red", "green", "yellow"]
REGION_PALLETE = ['#6baed6','#fd8d3c', '#74c476', '#9e9ac8']

COLORS_REGION = {
    'United States and Canada': "#6baed6", 
    'Latin America': "#fd8d3c",   
    'Europe,  Middle East and Africa': "#74c476",   
    'Asia-Pacific': "#9e9ac8"
    }

DEFAULT_QTRS = ['1', '2', '3', '4']
DEFAULT_YRS = ['2018']
DEFAULT_AREAS = ['United States and Canada', 'Latin America', 'Europe,  Middle East and Africa', 'Asia-Pacific']



###widgets###
OPTIONS_QTRS = ['1', '2', '3', '4']
OPTIONS_YEARS = ['2018', '2019', '2020']
OPTIONS_AREAS = ['United States and Canada', 'Latin America', 'Europe,  Middle East and Africa', 'Asia-Pacific']

#chart qtd
options_yr=OPTIONS_YEARS
button_group_yr=CheckboxButtonGroup(labels=options_yr)

options_qtr=OPTIONS_QTRS
button_group_qtr=CheckboxButtonGroup(labels=options_qtr)


#chart ytd
options_yr2=OPTIONS_YEARS
button_group_yr2=CheckboxButtonGroup(labels=options_yr2)

options_qtr2=OPTIONS_QTRS
button_group_qtr2=CheckboxButtonGroup(labels=options_qtr2)


#chart qtd_region
options_yr3=OPTIONS_YEARS
button_group_yr3=CheckboxButtonGroup(labels=options_yr3)

options_qtr3=OPTIONS_QTRS
button_group_qtr3=CheckboxButtonGroup(labels=options_qtr3)

options_area3=OPTIONS_AREAS
button_group_area3=CheckboxButtonGroup(labels=options_area3)


#chart ytd_region
options_yr4=OPTIONS_YEARS
button_group_yr4=CheckboxButtonGroup(labels=options_yr4)

options_qtr4=OPTIONS_QTRS
button_group_qtr4=CheckboxButtonGroup(labels=options_qtr4)

options_area4=OPTIONS_AREAS
button_group_area4=CheckboxButtonGroup(labels=options_area4)


#stacked bar chart ytd_region
options_yr5=OPTIONS_YEARS
button_group_yr5=CheckboxButtonGroup(labels=options_yr5)

options_qtr5=OPTIONS_QTRS
button_group_qtr5=CheckboxButtonGroup(labels=options_qtr5)

options_area5=OPTIONS_AREAS
button_group_area5=CheckboxButtonGroup(labels=options_area5)
