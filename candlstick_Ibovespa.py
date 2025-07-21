import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import mplfinance as mpf
import pandas as pd

inicio=dt.datetime(2024,1,1)
fim=dt.datetime(2025,6,30)

df = yf.download('^BVSP', start=inicio, end=fim)

if isinstance(df.columns, pd.MultiIndex): df.columns=df.columns.get_level_values(0)
if 'Adj Close' in df.columns: df = df.drop(columns=['Adj Close'])

df_ohlc_weekly = df.resample('7D').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'sum'
})

df_ohlc_weekly.dropna(inplace=True)

mpf.plot(
    df_ohlc_weekly,
    type='candle',
    style='charles',
    title='Ibovespa - Gráfico Semanal de Candlestick',
    volume=True,
    figsize=(12, 8)
)
plt.show()

