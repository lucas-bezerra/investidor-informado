from .joel_greenblatt import jg_main
from redislite import Redis
import fundamentus
import pandas as pd
import time
import json
import os
from io import StringIO

os.environ["TZ"] = "America/Sao_Paulo"
time.tzset()

redis_connection = Redis('/tmp/redis.db')


def get_papel(tickers):
    result = list()
    for ticker in tickers:
        ticker_data = fundamentus.get_papel(ticker)
        result.append(ticker_data)

    result = pd.concat(result)
    return result


def get_cache():
    cached_result = redis_connection.get('bg_list')
    if (cached_result):
        cached_result = json.loads(cached_result.decode())
        return cached_result
    else:
        return False


def set_cache(data):
    now = time.localtime()
    formated_date = time.strftime("%d/%m/%Y - %H:%M", now)

    data = json.dumps({
        "bg_list": data.to_json(),
        "date": formated_date
    })

    redis_connection.set('bg_list', data)
    redis_connection.expire('bg_list', 3600)


def create_df(ativos):
    Selic = 11.75
    rows = ativos[['Papel', 'Empresa', 'Setor',
                   'Subsetor', 'Cotacao', 'LPA', 'ROE', 'Div_Yield']]

    df = pd.DataFrame(rows, columns=[
                      'POS', 'Papel', 'Empresa', 'Setor', 'Subsetor', 'Cotacao', 'LPA', 'ROE', 'Div_Yield'])

    df.LPA = df.LPA.astype(float)/100
    df = df.loc[df['LPA'] > 0]

    df.ROE = [float(i.replace('%', ''))/100 for i in df.ROE.values]
    df.Div_Yield = [float(i.replace('%', ''))/100 for i in df.Div_Yield.values]

    df['Potencial de Crescimento'] = (
        df['ROE'] * (1 - (df['Div_Yield'] - df['LPA'])))
    df['Valor Justo'] = df['LPA'] * \
        ((100 / Selic + 3)) + (2 * df['ROE'] * df['Div_Yield']) * (1 / 1.15)
    df = df.sort_values('Potencial de Crescimento', ascending=False)

    df['Potencial de Crescimento'] = pd.Series(["{0:.2f}%".format(
        val * 100) for val in df['Potencial de Crescimento']], index=df.index)
    df['Dividend Yield'] = pd.Series(["{0:.2f}%".format(
        val * 100) for val in df['Div_Yield']], index=df.index)
    df['Cotação'] = pd.Series(
        ["R${0}".format(val) for val in df['Cotacao']], index=df.index)
    df['Valor Justo'] = pd.Series(["R${0}".format(
        round(val, 2)) for val in df['Valor Justo']], index=df.index)

    df['POS'] = range(1, len(df)+1)
    df = df.set_index('POS')

    df = df.reindex(columns=['Papel', 'Empresa', 'Setor', 'Subsetor', 'Cotação', 'Valor Justo', 'Dividend Yield',
                             'Potencial de Crescimento'])

    return df


def bg_main(update=False):
    tickers = jg_main()

    now = time.localtime()
    formated_date = time.strftime("%d/%m/%Y - %H:%M", now)

    if not (update):
        cached_result = get_cache()
        if (cached_result):
            bg_list = pd.read_json(StringIO(cached_result['bg_list']))
            list_date = cached_result['date']
            return bg_list, list_date

    ativos = get_papel(tickers)
    df = create_df(ativos)

    set_cache(df)

    return df, formated_date


# Remover comentário SOMENTE para testes locais
# if __name__ == '__main__':
#     result = bg_main(True)
