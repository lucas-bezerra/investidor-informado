from api.make_app import create_app
from api.methods.benjamin_graham import bg_main
from api.methods.fii import get_fiis
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

scheduler = BackgroundScheduler()
bg_job = scheduler.add_job(func=bg_main, args=[True], trigger='interval',
                           seconds=10800, name="Atualizando Tabela Preço Justo")
fii_job = scheduler.add_job(func=get_fiis, args=[True], trigger='interval',
                            seconds=10800, name="Atualizando Tabela FIIs")
scheduler.start()
