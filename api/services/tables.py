import pandas as pd
from io import StringIO
import time, json, os

os.environ["TZ"] = "America/Sao_Paulo"
time.tzset()

from redislite import Redis
redis_connection = Redis('/tmp/redis.db')

print(__package__)

from .methods.joel_greenblatt import jg_main
from .methods.benjamin_graham import bg_main

def get_data_from_cache_or_update():
    cached_result = redis_connection.get('tickers_list')

    if (cached_result):
      cached_result = json.loads(cached_result.decode())
      bg_list = pd.read_json(StringIO(cached_result['list']))
      list_date = cached_result['date']

      return bg_list, list_date
    else:
      print('Cache not found')
      bg_list, list_date = update_data()
      return bg_list, list_date

def update_data(is_post=False):
    now = time.localtime()
    formated_date = time.strftime("%d/%m/%Y - %H:%M", now)

    ttl = redis_connection.ttl('tickers_list')
    if (ttl > 1800):
       message = 'Sem alterações no momento'
       
       print(message)
       return message, formated_date

    jg_list = jg_main()
    bg_list = bg_main(jg_list)

    data = json.dumps({
      "list": bg_list.to_json(),
      "date": formated_date
    })

    redis_connection.set('tickers_list', data)
    redis_connection.expire('tickers_list', 3600)

    if (is_post):
      message = 'Lista Atualizada'
      return message, formated_date
    else:
      return bg_list, formated_date

def get_data():
    bg_list, list_date = get_data_from_cache_or_update()

    bg_list['Potencial de Crescimento'] = pd.Series(["{0:.2f}%".format(val * 100) for val in bg_list['Potencial de Crescimento']], index = bg_list.index)
    bg_list['Dividend Yield'] = pd.Series(["{0:.2f}%".format(val * 100) for val in bg_list['Div_Yield']], index = bg_list.index)
    bg_list['Cotação'] = pd.Series(["R${0}".format(val) for val in bg_list['Cotacao']], index = bg_list.index)
    bg_list['Valor Justo'] = pd.Series(["R${0}".format(round(val, 2)) for val in bg_list['Valor Justo']], index = bg_list.index)

    bg_list = bg_list.reindex(columns=['Papel', 'Empresa', 'Setor', 'Subsetor', 'Cotação', 'Valor Justo', 'Dividend Yield',
                                      'Potencial de Crescimento'])

    return bg_list, list_date

# get_data()