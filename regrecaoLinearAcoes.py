import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import seaborn as sns

inicio=dt.datetime(2024,1,1)
fim=dt.datetime(2025,6,30)

df1 = yf.download('GGBR4.SA', start=inicio, end=fim)
df2 = yf.download('PETR4.SA', start=inicio, end=fim)

df1_renomeado = df1[['Close']].rename(columns={'Close': 'Close_GGBR4'})
df2_renomeado = df2[['Close']].rename(columns={'Close': 'Close_PETR4'})

df_conj = df1_renomeado.join(df2_renomeado, how='inner')

ax=sns.regplot(x='Close_GGBR4', y='Close_PETR4', data=df_conj, color='black')
ax.set_xlabel('GGBR4',fontsize=16)
ax.set_ylabel('PETR4',fontsize=16)
plt.show()

jp = sns.jointplot(x='Close_GGBR4', y='Close_PETR4', data=df_conj, kind='scatter', color='black')
jp.set_axis_labels('GGBR4', 'PETR4', fontsize=16)
plt.show()