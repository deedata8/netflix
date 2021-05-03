import pandas as pd

df = pd.read_csv('data/Netflix.csv')

#trim off spaces in column headings
df.rename(columns=lambda x: x.strip(), inplace=True)

#clean data, convert to numeric
df['Revenue'] = df['Revenue'].str.replace(',', '').astype(float)
df['Subscribers'] = df['Subscribers'].str.replace(',', '').astype(float)
df['Qtr'] = pd.to_numeric(df['Years'].str[1:2])
df['Year'] = pd.to_numeric(df['Years'].str[5:])
df.dropna(inplace=True)

#chart df in in millions
chart_df = df.groupby(['Year', 'Qtr']).sum()/1000000

#get qtr(s) and yr(s) to present in chart
def groupings(list_qtrs, list_yrs):
    q = []
    y = []
    
    for n in range(len(list_qtrs)):
        for i in range(len(list_yrs)):
            q.append(list_qtrs[n])
    
    for n in range(len(list_qtrs)):
        for j in list_yrs:
            y.append(j)

    tuple_ = list(zip(q,y))
    return tuple_

#get revenue based on qtr and yr
def get_rev(list_tups):
    list_y = []
    for i, ii in list_tups:
        try:
            df = chart_df.query('Year == @ii and Qtr == @i' )
            list_y.append(df.Revenue.values[0])
        except:
            list_y.append(0)
            pass
    return list_y

#get subscriber count based on qtr and yr
def get_subs(list_tups):
    list_y = []
    for i, ii in list_tups:
        try:
            df = chart_df.query('Year == @ii and Qtr == @i' )
            list_y.append(df.Subscribers.values[0])
        except:
            list_y.append(0)
            pass
    return list_y