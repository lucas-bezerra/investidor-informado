"""
resultado:
    Info from http://fundamentus.com.br/fii_resultado.php
"""


import fundamentus.utils as utils

import requests
import requests_cache
import pandas as pd
import time
import logging

from tabulate import tabulate


def get_resultado_raw_fii():
    """
    Get data from fundamentus:
      URL:
        http://fundamentus.com.br/fii_resultado.php

    RAW:
      DataFrame preserves original HTML header names

    Output:
      DataFrame
    """

    ##
    # Busca avançada por empresa
    ##
    url = 'http://www.fundamentus.com.br/fii_resultado.php'
    hdr = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
           'Accept': 'text/html, text/plain, text/css, text/sgml, */*;q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           }

    with requests_cache.enabled():
        content = requests.get(url, headers=hdr)

        if content.from_cache:
            logging.debug('.../fii_resultado.php: [CACHED]')
        else:  # pragma: no cover
            logging.debug('.../fii_resultado.php: sleeping...')
            time.sleep(.500)  # 500 ms

    # parse + load
    df = pd.read_html(content.text, decimal=",", thousands='.')[0]

    # Fix: percent string
    df['Dividend Yield'] = utils.perc_to_float(df['Dividend Yield'])

    # index by 'Papel', instead of 'int'
    df.index = df['Papel']
    df.drop('Papel', axis='columns', inplace=True)
    df.sort_index(inplace=True)

    # naming
    df.name = 'Fundamentus: HTML names'
    df.columns.name = 'Multiples'
    df.index.name = 'papel'

    # return sorted by 'papel'
    return df


def get_resultado_fii():
    """
    Data from fundamentus, fixing header names.
      URL:
        http://fundamentus.com.br/fii_resultado.php
      Obs:
        DataFrame uses short header names
    Output:
      DataFrame
    """

    # get RAW data
    data1 = get_resultado_raw_fii()

    # rename!
    data2 = _rename_cols_fii(data1)

    # metadata
    data2.name = 'Fundamentus: short names'
    data2.columns.name = 'Multiples'
    data2.index.name = 'papel'

    # remove duplicates
#   df = data2.drop_duplicates(subset=['cotacao','pl','pvp'], keep='last')
    df = data2.drop_duplicates(keep='first')

    return df


def _rename_cols_fii(data):
    """
    Rename columns in DataFrame
      - use a valid Python identifier
      - so each column can be a DataFrame property
      - Example:
          df.pl > 0
    """

    df2 = pd.DataFrame()

    # Fix: rename columns
    df2['cotacao'] = data['Cotação']
    df2['dy'] = data['Dividend Yield']
    df2['pvp'] = data['P/VP']
    df2['vlm'] = data['Valor de Mercado']
    df2['liq'] = data['Liquidez']
    df2['qtdi'] = data['Qtd de imóveis']
    df2['capr'] = data['Cap Rate']
    df2['vacm'] = data['Vacância Média']

    return df2
