from api.make_app import create_app
from api.methods.benjamin_graham import bg_main
from api.methods.fii import get_fiis
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

def prevent_inactivity():
  import requests

  result = requests.get('https://investidor-informado.onrender.com/')
  print(result)
  return True


scheduler = BackgroundScheduler()
bg_job = scheduler.add_job(func=bg_main, args=[True], trigger='interval',
                           seconds=10800, name="Atualizando Tabela Preço Justo")
fii_job = scheduler.add_job(func=get_fiis, args=[True], trigger='interval',
                            seconds=10800, name="Atualizando Tabela FIIs")
delay_job = scheduler.add_job(func=prevent_inactivity, trigger='interval',
                            seconds=780, name="Previnir inatividade da aplicação no Render.com")
scheduler.start()
