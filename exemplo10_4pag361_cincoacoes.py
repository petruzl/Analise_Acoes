import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf

inicio=dt.datetime(2024,1,1)
fim=dt.datetime(2025,6,30)

acoes=['GGBR4.SA', 'BBAS3.SA', 'PETR4.SA', 'USIM5.SA', 'ITUB4.SA']
df = yf.download(acoes, start=inicio, end=fim)
df['Data']=df.index

dados=df['Close'].plot(style=['-', '--', '-o', '-*', '-d'],color='k', lw=1)
dados.set_xlabel('data',fontsize=16)
dados.set_xlabel('acoes',fontsize=16)
plt.grid(True)
plt.title('AÇOES (JAN/24 A JUN/25)',fontsize=18,weight='bold')
plt.legend(acoes)
plt.show()