from flask import Blueprint, render_template

from .methods.benjamin_graham import bg_main
from .methods.fii import get_fiis


panels = Blueprint('panels', __name__)


@panels.route('/preco-justo')
def preco_justo():
    bg_list, list_date = bg_main()
    return render_template('panels/preco_justo.html',
                           tables=[bg_list.to_html(
                               classes='table table-hover table-striped', index=True, index_names='POS', border=0)],
                           titles=bg_list.columns.values,
                           list_date=list_date)


@panels.route('/fiis')
def fiis():
    fii_list, list_date = get_fiis()
    return render_template('panels/fii.html',
                           tables=[fii_list.to_html(
                               classes='table table-hover table-striped', index=True, index_names='Ranking', border=0)],
                           titles=fii_list.columns.values,
                           list_date=list_date)
