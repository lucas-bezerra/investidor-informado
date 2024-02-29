import fundamentus
import pandas as pd

from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import multiprocessing

def get_papel_threaded(tickers):
    result = list()
    for ticker in tickers:
        ticker_data = fundamentus.get_papel(ticker)
        result.append(ticker_data)

    result = pd.concat(result)
    return result

def bg_main(tickers):
    batch_size = 2 # Tamanho do lote
    # Dividir os dados em lotes
    batches = [tickers[i:i+batch_size] for i in range(0, len(tickers), batch_size)]

    # Processar lotes em paralelo
    with multiprocessing.get_context("spawn").Pool() as pool:
      processed_batches = list(tqdm(pool.imap(get_papel_threaded, batches), total=len(batches), desc='COLETANDO DADOS DAS AÇÕES'))

    # Juntar os lotes processados
    ativos = pd.concat(processed_batches).reset_index()

    Selic = 11.75
    rows = ativos[['Papel', 'Empresa', 'Setor', 'Subsetor', 'Cotacao', 'LPA', 'ROE', 'Div_Yield']]

    df = pd.DataFrame(rows, columns=['Papel', 'Empresa', 'Setor', 'Subsetor', 'Cotacao', 'LPA', 'ROE', 'Div_Yield'])

    df.LPA = df.LPA.astype(float)/100
    df = df.loc[df['LPA'] > 0]

    df.ROE = [float(i.replace('%', ''))/100 for i in df.ROE.values]
    df.Div_Yield = [float(i.replace('%', ''))/100 for i in df.Div_Yield.values]

    df['Potencial de Crescimento'] = (df['ROE'] * (1 - (df['Div_Yield'] - df['LPA'])))
    df['Valor Justo'] = df['LPA'] * ((100 / Selic + 3)) + (2 * df['ROE'] * df['Div_Yield']) * (1 / 1.15)
    df = df.sort_values('Potencial de Crescimento', ascending=False)

    return df

# Remover comentário SOMENTE para testes locais
# if __name__ == '__main__':
#     result = bg_main(['PETR4', 'PETR3', 'CMIN3', 'CMIG4', 'VALE3'])