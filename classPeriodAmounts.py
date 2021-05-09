class PeriodAmounts():
    
    """Return QTD or YTD Revenue and Subscriber count"""
    
    #required params at instantiation
    def __init__(self, dataframe):
        #df by 'Qtr', 'Year', and 'Area' for revenue and subscribers-- lowest level
        self.df = dataframe
    
    
    def groupby_yq(self):
        df_ = self.df.groupby(['Year', 'Qtr']).sum()
        return df_
    
    #qtr, yr, [area] in args -> returns rev, subs count
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
        print("FROM CLASS REV", qtd_rev)
        return qtd_rev, qtr_sub
    
    #qtr, yr, [area] in args -> returns rev, subs count
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
                    for i in range(1, int(q)+1):
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
                    for i in range(1, int(q)+1):
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

    #data structures for bokeh stacked bar chart       
    #list of (qtr,yr,[]) tuple, and list of area in args -> returns dict = 'x':[(qtr-yr)], area:[rev] for CDS
    def get_area_y_ytd(self, data_refs_qy: tuple, area:list) -> dict:
        region = ['United States and Canada', 'Latin America', 'Europe,  Middle East and Africa', 'Asia-Pacific']
        ytd_sub = []
        dict_ = {}
        qtr_yr = []
        #exclude [blank area] in tuples
        for i in data_refs_qy:
            qtr_yr.append(i[:2])
        dict_['x'] = qtr_yr

        #below queries for only the region selected
        for r in region:
            ytd_rev = []
            for q, y in qtr_yr:
                y_rev = 0
                #for row, sum with prior quarters based on area
                for i in range(1, int(q)+1):
                    if r in area:
                        try:
                            row = self.df.query('Year == @y and Qtr == @i and Area == @r' )
                            y_rev += row.iloc[0]['Revenue']
                        except:
                            y_rev = 0
                    else:
                        y_rev = 0
                ytd_rev.append(y_rev)
            dict_[r] = ytd_rev

        return dict_


# from data import dataframe
# factors = [('2', '2020', ''), ('2', '2019', '')] 
# b = ['Europe,  Middle East and Africa', 'Asia-Pacific']
# chart1 = PeriodAmounts(dataframe)
# source = chart1.get_area_y_ytd(factors, b)
# print(source)
    






