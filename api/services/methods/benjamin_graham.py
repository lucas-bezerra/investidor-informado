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
    ativos = get_papel_threaded(tickers)

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