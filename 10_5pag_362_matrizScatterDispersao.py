import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import pandas as pd

inicio=dt.datetime(2024,1,1)
fim=dt.datetime(2025,6,30)

acoes=['GGBR4.SA', 'BBAS3.SA', 'PETR4.SA', 'USIM5.SA', 'ITUB4.SA']
df = yf.download(acoes, start=inicio, end=fim)
retorno=df['Close'].pct_change()
pd.plotting.scatter_matrix(retorno, diagonal='kde',alpha=0.8, color='black')
plt.show()
