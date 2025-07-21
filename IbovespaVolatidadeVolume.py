import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf

inicio=dt.datetime(1995,1,1)
fim=dt.datetime(2025,6,30)

df = yf.download('^BVSP', start=inicio, end=fim)
df['retorno']=df['Close'].pct_change()
#df['retorno'].plot(color='k', lw=2, alpha=0.4)
df['med_mov']=df['Close'].rolling(window=500,min_periods=0).mean()
df['std_mov']=df['retorno'].rolling(window=10,min_periods=0).std()

ax=plt.subplot(311)
ax.plot(df.index, df['Close'],color='black',alpha=0.5)
ax.plot(df.index, df['med_mov'],color='black')
ax.set_title('Ibovespa(1995-2025)', fontsize=18, weight='bold')

ax=plt.subplot(312)
ax.plot(df.index, df['retorno'],color='black',alpha=0.5)
ax.plot(df.index, df['std_mov'],color='black')
ax.set_title('Volatidade retorno Ibovespa (1995-2025)', fontsize=18, weight='bold')

plt.tight_layout()
#plt.grid()

ax=plt.subplot(313)
df['Volume'].plot(kind='bar',color='black')
ax.set_title('Volume Ibovespa (1995-2025)', fontsize=18, weight='bold')

#plt.title('Retorno financerio Ibovespa Jan/1995 a jun/25', fontsize=18, weight='bold')
#plt.legend(['Ibovespa', 'Volatidade(desv.padrão)10 dias'])
plt.show()