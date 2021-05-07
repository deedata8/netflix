import pandas as pd

df = pd.read_csv('data/Netflix.csv')

#trim off spaces in column headings
df.rename(columns=lambda x: x.strip(), inplace=True)

#clean data, convert to numeric
df['Revenue'] = df['Revenue'].str.replace(',', '').astype(float)
df['Subscribers'] = df['Subscribers'].str.replace(',', '').astype(float)
df['Area'] = df['Area'].str.replace(',', '')
df['Qtr'] = pd.to_numeric(df['Years'].str[1:2])
df['Year'] = pd.to_numeric(df['Years'].str[5:])
df.drop(columns=['Years'], inplace=True)
df.dropna(inplace=True)

dataframe = df.groupby(['Year', 'Qtr', 'Area']).sum()/1000000

#chart df in in millions
chart_df = df.groupby(['Year', 'Qtr']).sum()/1000000

#get qtr, yr, [area] tuples to present in charts
def groupings(qtrs:list, yrs:list, areas:list=[]) -> tuple:
    q, y, a = [], [], []
    
    if len(areas) > 0:
        #start with most narrow grouping
        for n in range(len(areas)):
            for i in qtrs:
                for j in yrs:
                    a.append(areas[n])
                    q.append(i)
                    y.append(j)
        
    else: 
        for n in range(len(qtrs)):
            for j in yrs:
                q.append(qtrs[n])
                y.append(j)
                a.append("")
    
    tuple_ = list(zip(q,y,a))
    return tuple_


