
class PeriodAmounts():
    
    """Return QTD or YTD Revenue and Subscriber count"""
    
    #required params at instantiation
    def __init__(self, dataframe):
        #df by 'Qtr', 'Year', and 'Area' for revenue and subscribers-- lowest level
        self.df = dataframe
    
    
    def groupby_yq(self):
        df_ = self.df.groupby(['Year', 'Qtr']).sum()
        return df_
    
    
    def get_qtd(self, data_refs: tuple) -> list:
        qtd_rev = []
        qtr_sub = []
        #if no Area listed in input tuples
        if data_refs[0][2] == "":
            df_ = self.groupby_yq()
            for q, y, a in data_refs:
                try:
                    row = df_.query('Qtr == @q and Year == @y' )
                    qtd_rev.append(row.Revenue.values[0])
                    qtr_sub.append(row.Subscribers.values[0])
                except:
                    #revenue is zero if qtr-yr doesn't exist (data_refs may include qtrs/yrs that have no data)
                    qtd_rev.append(0)
                    qtr_sub.append(0)
        else:
            for q, y, a in data_refs:
                try:
                    row = self.df.query('Qtr == @q and Year == @y and Area == @a' )
                    qtd_rev.append(row.Revenue.values[0])
                    qtr_sub.append(row.Subscribers.values[0])
                except:
                    qtd_rev.append(0)
                    qtr_sub.append(0)
                
        return qtd_rev, qtr_sub
    
    
    def get_ytd(self, data_refs: tuple) -> list:
        ytd_rev = []
        ytd_sub = []
        #if no Area listed in input tuples
        if data_refs[0][2] == "":
            df_ = self.groupby_yq()
            for q, y, a in data_refs:
                y_rev = 0
                try:
                    #for each row, sum with prior quarters
                    for i in range(1, q+1):
                        row = df_.query('Year == @y and Qtr == @i')
                        y_rev += row.iloc[0]['Revenue']
                    ytd_rev.append(y_rev)

                    row = df_.query('Year == @y and Qtr == @q')
                    y_sub = row.iloc[0]['Subscribers']
                    ytd_sub.append(y_sub)
                except:
                    ytd_rev.append(0)
                    ytd_sub.append(0)
        else:
            for q, y, a in data_refs:
                y_rev = 0
                try:
                    #for row, sum with prior quarters based on area
                    for i in range(1, q+1):
                        row = self.df.query('Year == @y and Qtr == @i and Area == @a' )
                        y_rev += row.iloc[0]['Revenue']
                    ytd_rev.append(y_rev)

                    row = self.df.query('Year == @y and Qtr == @q and Area == @a')
                    y_sub = row.iloc[0]['Subscribers']
                    ytd_sub.append(y_sub)
                except:
                    ytd_rev.append(0) 
                    ytd_sub.append(0)
    
        return ytd_rev, ytd_sub


# from df import data
# from df import groupings

# t = groupings([1,2,3,4], [2018,2019,2020])
# t2 = groupings([2,3,4], [2018,2019,2020], ['United States and Canada','Latin America','Asia-Pacific'])

# #print(t)
# print(t2)

# amounts = PeriodAmounts(data)
# revs, subs = amounts.get_ytd(t2)
# print('REV', revs)
# print('SUBS', subs)