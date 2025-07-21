import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf

inicio=dt.datetime(1995,1,1)
fim=dt.datetime(2025,6,30)

df = yf.download('^BVSP', start=inicio, end=fim)
df['retorno']=df['Close'].pct_change()
df['retorno'].plot(color='k', lw=2, alpha=0.4)
df['std_mov']=df['retorno'].rolling(window=10,min_periods=0).std()
df['std_mov'].plot(color='k', lw=3, style='-')

plt.grid()
plt.title('Retorno financerio Ibovespa Jan/1995 a jun/25', fontsize=18, weight='bold')
plt.legend(['Ibovespa', 'Volatidade(desv.padrão)10 dias'])
plt.show()