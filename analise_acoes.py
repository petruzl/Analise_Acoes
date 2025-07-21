import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
#import pandas_datareader.data as web

inicio=dt.datetime(2024,1,1)
fim=dt.datetime(2025,6,30)
#df=web.DataReader('PETR4.SA','yahoo',inicio,fim)
df = yf.download('PETR4.SA', start=inicio, end=fim)

df['Close'].plot(color='k',lw=4)
plt.grid()
plt.title('PETR4 (Jan/2024 a Junho/25)',fontsize=18,weight='bold')
plt.show()
#print(df['Close'].head(5))
print(df['Close'].tail(5))