from api.make_app import create_app
from api.services.tables import update_data
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

scheduler = BackgroundScheduler()
job = scheduler.add_job(func=update_data, trigger='interval', seconds=1800, name="Atualizando Dados das Tabelas")
scheduler.start()