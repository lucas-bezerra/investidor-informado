from ..fundamentus_fii import fii, resultado_fii, utils
import pandas as pd
import json
import time
from io import StringIO
from redislite import Redis
redis_connection = Redis('/tmp/redis.db')


def filter_info():
    # Exibindo o dataframe conforme o site Fundamentus
    df = resultado_fii.get_resultado_fii()

    # Filtrando conforme aplicado pela formula
    # Liq >= R$1.000.000,00
    # Div. Yield >= 6%
    filtro = df[(df['liq'] >= 1000000) & (df['dy'] >= 0.06)]

    return filtro


def rank_info(filtro):
    # Criando o dataframe
    df = pd.DataFrame()

    # Criando um range que vá de 1 até o número de ativos existentes no filtro
    df['POS'] = range(1, len(filtro)+1)

    # P/VP - do menor para o maior
    df['P/VP'] = filtro.sort_values(by=['pvp'],
                                    ascending=True).index[:len(filtro)].values

    # Dividend Yield - do maior para o menor
    df['DY'] = filtro.sort_values(
        by=['dy'], ascending=False).index[:len(filtro)].values

    return df


def create_table(df):
    a = df.pivot_table(columns='P/VP', values='POS')
    b = df.pivot_table(columns='DY', values='POS')
    t = pd.concat([a, b])
    rank = t.dropna(axis=1).sum()
    dataframe = pd.DataFrame(rank.sort_values())

    return dataframe


def get_papel(tickers):
    result = list()
    for ticker in tickers:
        ticker_data = fii.get_detalhes_fii(ticker)
        result.append(ticker_data)

    result = pd.concat(result)
    return result


def get_cache():
    cached_result = redis_connection.get('fii_list')
    if (cached_result):
        cached_result = json.loads(cached_result.decode())
        return cached_result
    else:
        return False


def set_cache(data):
    now = time.localtime()
    formated_date = time.strftime("%d/%m/%Y - %H:%M", now)

    data = json.dumps({
        "fii_list": data.to_json(),
        "date": formated_date
    })

    redis_connection.set('fii_list', data)
    redis_connection.expire('fii_list', 432000)


def get_fiis(update=False):
    now = time.localtime()
    formated_date = time.strftime("%d/%m/%Y - %H:%M", now)

    if not (update):
        cached_result = get_cache()
        if (cached_result):
            fii_list = pd.read_json(StringIO(cached_result['fii_list']))
            list_date = cached_result['date']
            return fii_list, list_date

    filtro = filter_info()
    ranking = rank_info(filtro)
    dataframe = create_table(ranking)
    tickers = list(dataframe.index)
    fiis = get_papel(tickers)

    fiis['Cotação'] = pd.Series(
        ["R${0}".format(val) for val in fiis['Cotacao']], index=fiis.index)

    fiis['Dividend Yield'] = pd.Series(fiis['Div_Yield'], index=fiis.index)

    fiis['PVP'] = utils.perc_to_float(fiis['PVP'])
    fiis['P/VP'] = pd.Series(["{:,.2f}".format(val).replace(",", ".")
                             for val in fiis['PVP']], index=fiis.index)

    fiis['Dividendocota'] = utils.perc_to_float(fiis['Dividendocota'])
    fiis['Div./Cota (12m)'] = pd.Series(["R${:,.2f}".format(
        val).replace(",", ".") for val in fiis['Dividendocota']], index=fiis.index)

    rows = fiis[['FII', 'Nome', 'Segmento', 'Mandato',
                 'Cotação', 'PVP', 'Dividend Yield', 'Div./Cota (12m)']]

    df = pd.DataFrame(rows, columns=[
                      'POS', 'FII', 'Nome', 'Segmento', 'Mandato',
                      'Cotação', 'PVP', 'Dividend Yield', 'Div./Cota (12m)'])

    df = df.fillna('')
    df['POS'] = range(1, len(df)+1)
    df = df.set_index('POS')
    set_cache(df)

    return df, formated_date


# get_fiis(True)
