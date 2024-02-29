from flask import Blueprint, render_template

from .services.tables import get_data, update_data

panels = Blueprint('panels', __name__)

@panels.route('/preco-justo')
def preco_justo():
    bg_list, list_date = get_data()
    return render_template('panels/preco_justo.html',
                           tables=[bg_list.to_html(classes='table table-hover table-striped table-dark table-responsive', index = False, border=0)],
                           titles=bg_list.columns.values,
                           list_date=list_date)

@panels.route('/update-cache', methods=['POST'])
def update_cache():
    message, formated_date = update_data(True)
    print('Dados Atualizados com sucesso! - ', formated_date)
    return message