import sqlite3
import pandas as pd
import plotly as py
import plotly.graph_objs as go

#db
db_name="C:/Users/bokue/OneDrive/Workspace/DB/kabu.db"
conn=sqlite3.connect(db_name)
c=conn.cursor()

##DBを見る
# df=pd.read_sql("select * from kabuayumine where tradetime in('1130','1500') group by meig_c,tradeymd,tradetime ",conn)
# df=pd.read_sql("select * from meig_mst ",conn)
# print(df)
df1=pd.read_sql("select meig_c,substr(tradeymd,1,4) || '-' ||substr(tradeymd,5,2) || '-'|| substr(tradeymd,7,2) as tradeymd,count(tradeymd) trade_count from (select * from (select meig_c,tradeymd,tradetime,count(tradetime) as countTick from kabuayumine  group by meig_c,tradeymd,tradetime) where  countTick >=15) group by meig_c,tradeymd",conn)
#df1 = pd.DataFrame(df,columns=['meig_nm','volume'])
# print(df1)
df=pd.read_sql("select substr(tradeymd,1,4) || '-' ||substr(tradeymd,5,2) || '-'|| substr(tradeymd,7,2) as tradeymd,open_price,high_price,low_price,close_price,volume from meig_price where tradeymd > '20180911'order by tradeymd",conn)
#print(df)
#trace = go.Candlestick(x=df.tradeymd1, open=df.open_price, high=df.high_price, low=df.low_price, close=df.close_price)
#py.offline.plot([trace], filename='fx_plotly_candlestick')
trace1 = go.Candlestick(x=df.tradeymd, 
                        open=df.open_price, 
                        high=df.high_price, 
                        low=df.low_price, 
                        close=df.close_price,
                        line=dict(
                            width=1
                        ),
                        increasing=dict(
                            line=dict(
                                color='#ff0000'
                            ),
                            fillcolor='#ff0000'
                        ),
                        decreasing=dict(
                            line=dict(
                                color='#0019ff'
                            ),
                            fillcolor='#0019ff'
                        )
                        )

trace2 = go.Scatter(
    x=df1.tradeymd,
    y=df1.trade_count,
    name='HotLevel',
    yaxis='y2',
        line=dict(
        width=1
    )
)

trace3 = go.Candlestick(x=df.tradeymd, 
                        open=[0], 
                        high=df.volume, 
                        low=[0], 
                        close=df.volume,
                        line=dict(
                            width=1
                        ),
                        increasing=dict(
                            line=dict(
                                color='#ff0000'
                            ),
                            fillcolor='#ff0000'
                        )
                        )
data = [trace1, trace2]
layout = go.Layout(
    title='韭菜们的热度',
   
    xaxis=dict(
        domain=[0.3, 0.7]
    ),
    yaxis=dict(
        title='株価',
        titlefont=dict(
            color='#1f77b4'
        ),
        tickfont=dict(
            color='#1f77b4'
        ),

    ),
    yaxis2=dict(
        title='热度（＞15回Ticks／分）',
        titlefont=dict(
            color='#ff7f0e'
        ),
        tickfont=dict(
            color='#ff7f0e'
        ),
        anchor='free',
        overlaying='y',
        side='right',
        position=0.72
    )
    # yaxis3=dict(
    #     title='出来高',
    #     titlefont=dict(
    #         color='#ff7f0e'
    #     ),
    #     tickfont=dict(
    #         color='#ff7f0e'
    #     ),
    #     anchor='free',
    #     overlaying='y',
    #     side='bottom',
    #     position=0.2
    # )
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.offline.plot(fig, filename='multiple-axes-multiple')
