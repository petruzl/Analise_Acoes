import pandas as pd
import requests

# URL da tabela de ações listadas no site Fundamentus
url = 'http://www.fundamentus.com.br/resultado.php'

# Definir um User-Agent para simular um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    # Fazer a requisição GET com os cabeçalhos personalizados
    response = requests.get(url, headers=headers)
    response.raise_for_status() # Lança um HTTPError para respostas de erro (4xx ou 5xx)

    # Ler a tabela da página a partir do conteúdo HTML da resposta
    # Usamos io=response.text para passar o conteúdo HTML diretamente
    tabelas = pd.read_html(response.text, decimal=',', thousands='.')

    # A tabela que queremos normalmente é a primeira na lista retornada
    df = tabelas[0]

    # Verificando as primeiras linhas da tabela
    print("DataFrame original do Fundamentus:")
    print(df.head())
    print(df.columns)

    # Extraindo coluna de Tickers e formatando para Yahoo Finance
    if 'Papel' in df.columns:
        df['TickerYahoo'] = df['Papel'] + '.SA'
    else:
        raise ValueError("Coluna 'Papel' não encontrada no DataFrame. Verifique a estrutura da tabela do Fundamentus.")

    print("\nLista de tickers da B3 (exemplo):")
    print(df['TickerYahoo'].head(10))

    # Salvar lista em CSV para uso futuro
    df.to_csv('fundamentus_acao_lista.csv', index=False)
    print("\nLista de ações salva em 'fundamentus_acao_lista.csv'.")

except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar a URL: {e}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

