import pandas as pd
import yfinance as yf
import datetime as dt

# --- Parte 1: Carregar a lista de ações do CSV ---
try:
    df_acoes = pd.read_csv('fundamentus_acao_lista.csv')
    # Se a coluna 'TickerYahoo' já existe e está correta, use-a.
    # Caso contrário, crie-a novamente, supondo que 'Papel' é o ticker B3.
    if 'TickerYahoo' not in df_acoes.columns:
        if 'Papel' in df_acoes.columns:
            df_acoes['TickerYahoo'] = df_acoes['Papel'] + '.SA'
        else:
            print("Erro: A coluna 'Papel' ou 'TickerYahoo' não foi encontrada no CSV.")
            exit()

    # Pega apenas os tickers únicos e válidos
    tickers_validos = df_acoes['TickerYahoo'].dropna().unique().tolist()
    print(f"Total de {len(tickers_validos)} tickers carregados do CSV.")

except FileNotFoundError:
    print("Erro: O arquivo 'fundamentus_acao_lista.csv' não foi encontrado. Execute o script de coleta de ações primeiro.")
    exit()
except Exception as e:
    print(f"Erro ao carregar ou processar o CSV: {e}")
    exit()

# --- Parte 2: Iterar sobre os tickers e aplicar filtros ---

# Lista para armazenar as ações que passaram nos filtros
acoes_filtradas = []

# Definir a data limite para o histórico de dividendos (10 anos atrás)
data_limite_dividendos = pd.Timestamp.today() - pd.DateOffset(years=10)

# Contador para acompanhar o progresso
processadas = 0
total_tickers = len(tickers_validos)

print("\nIniciando a filtragem das ações (isso pode levar um tempo, pois acessa a API do Yahoo Finance para cada ação)...")

# Opcional: limitar o número de ações para teste rápido
# tickers_para_analisar = tickers_validos[:50] # Analisa apenas as primeiras 50 para teste
tickers_para_analisar = tickers_validos # Analisa todas as ações

for ticker_yf in tickers_para_analisar:
    processadas += 1
    print(f"Processando {processadas}/{total_tickers}: {ticker_yf}")

    try:
        acao = yf.Ticker(ticker_yf)
        info = acao.info # Dados fundamentais

        # 1. Obter histórico de dividendos
        dividendos = acao.dividends
        # Remover o timezone para comparação, se existir
        if not dividendos.empty and dividendos.index.tz is not None:
            dividendos.index = dividendos.index.tz_localize(None)

        # Verificar se pagou dividendos em cada um dos últimos 10 anos
        pagou_em_todos_anos_passados = True
        if dividendos.empty: # Se não pagou nenhum dividendo, já falha o filtro
            pagou_em_todos_anos_passados = False
        else:
            # Pega o ano atual e o ano 10 anos atrás
            ano_atual = pd.Timestamp.now().year
            ano_dez_anos_atras = ano_atual - 10

            # Verifica se houve pagamento em cada ano dentro do período
            for ano in range(ano_dez_anos_atras, ano_atual + 1):
                # Filtra dividendos para o ano específico
                dividendos_no_ano = dividendos[dividendos.index.year == ano]
                if dividendos_no_ano.empty:
                    pagou_em_todos_anos_passados = False
                    break # Se falhou em um ano, não precisa verificar mais
            # Adicionalmente, verifica se há pelo menos um dividendo dentro do período total de 10 anos
            if not dividendos[dividendos.index >= data_limite_dividendos].empty:
                pagou_dividendos_nos_ultimos_10_anos_geral = True
            else:
                pagou_dividendos_nos_ultimos_10_anos_geral = False
            
            # Combine as duas condições de dividendo:
            # 1. Teve algum dividendo nos últimos 10 anos (geral)
            # 2. Teve dividendo em cada um dos últimos 10 anos (mais rigoroso)
            # Escolha qual regra você quer (a segunda é bem mais rigorosa)
            pagou_dividendos_ok = pagou_dividendos_nos_ultimos_10_anos_geral and pagou_em_todos_anos_passados
        
        # Obter dados fundamentais (com verificação para evitar None)
        price = info.get('currentPrice')
        book_value = info.get('bookValue')
        total_debt = info.get('totalDebt') # Total Debt
        net_income = info.get('netIncomeToCommon') # Lucro Líquido
        
        # Yahoo Finance pode não ter todos esses dados, ou podem ser 0/None
        # Verificar se os dados necessários existem antes de comparar
        if (price is None or book_value is None or
            total_debt is None or net_income is None):
            # print(f"  Dados fundamentais incompletos para {ticker_yf}. Pulando.")
            continue # Pula esta ação se os dados estiverem incompletos

        # Aplicar os filtros
        # Critério 2: Preço > Valor Contábil (Originalmente 'menor que o preço atual', o que é estranho.
        # Assumi o oposto: se o preço atual é menor que o valor contábil, a ação estaria 'barata' em relação ao patrimônio.
        # Vou usar P/VP < 1, que significa preço < valor contábil)
        # P/VP = Preço / Valor Contábil por Ação
        # Se P/VP não é dado, podemos calcular:
        pvp = price / book_value if book_value != 0 else float('inf') # Evita divisão por zero

        # Critério 3: Dívida líquida <= 0 e lucro líquido > 0
        # Yahoo Finance fornece 'totalDebt', não diretamente 'dívida líquida'.
        # Vamos assumir 'totalDebt' para este filtro. Um valor <= 0 pode indicar caixa líquido.
        
        # O Fundamentus pode ter "Dív.Brut/ Patrim." (Dívida Bruta/Patrimônio)
        # Se você quer usar essa informação, teria que puxar do dataframe inicial
        # e converter para numérico. Por simplicidade, usando 'totalDebt' do yfinance.

        # Verificar todos os critérios
        if (pagou_dividendos_ok and
            pvp < 1 and # Preço por ação menor que o valor contábil (P/VP < 1)
            total_debt <= 0 and # Não ter dívida (ou ter caixa líquido positivo)
            net_income > 0): # Ter lucro
            
            acoes_filtradas.append({
                'Ticker': ticker_yf,
                'Preco': price,
                'Valor_Contabil': book_value,
                'P/VP': pvp,
                'Divida_Total': total_debt,
                'Lucro_Liquido': net_income
            })
            print(f"  {ticker_yf} PASSOU em TODOS os filtros!")
        # else:
            # print(f"  {ticker_yf} não passou nos filtros. Detalhes: Div:{pagou_dividendos_ok}, P/VP<1:{pvp < 1}, Divida<=0:{total_debt <= 0}, Lucro>0:{net_income > 0}")

    except Exception as e:
        print(f"  Erro ao processar {ticker_yf}: {e}")
        # print(f"  Erro completo: {e}")
        continue # Continua para a próxima ação mesmo com erro

# --- Parte 3: Apresentar resultados ---
df_acoes_filtradas = pd.DataFrame(acoes_filtradas)

if not df_acoes_filtradas.empty:
    print(f"\n--- Análise Concluída: {len(df_acoes_filtradas)} ações passaram nos filtros ---")
    print(df_acoes_filtradas)
    df_acoes_filtradas.to_csv('acoes_filtradas_por_fundamentos.csv', index=False)
    print("\nResultados salvos em 'acoes_filtradas_por_fundamentos.csv'.")
else:
    print("\n--- Análise Concluída: Nenhuma ação passou em todos os filtros. ---")

