import requests
import pandas as pd

url = 'https://www.infomoney.com.br/cotacoes/empresas-b3/'
tables = pd.read_html(url)
acoes = tables[1]['Ativos']
print(acoes)
