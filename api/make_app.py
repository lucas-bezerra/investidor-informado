from flask import Flask, render_template
from flask_cors import CORS


def create_app():
    app = Flask(__name__,
                static_url_path='',
                static_folder='static')

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for panels parts of app
    from .panels import panels as panels_blueprint
    app.register_blueprint(panels_blueprint)

    # Função para renderizar uma página de erro personalizada
    def render_error_page(error):
        return render_template('errors/error.html', error=error), error.code

    # Adicione a função ao manipulador de erros para o código de status 404
    @app.errorhandler(404)
    def page_not_found(error):
        return render_error_page(error)

    # Adicione a função ao manipulador de erros para o código de status 500
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_error_page(error)

    # Rota de exemplo para gerar um código de status 404
    @app.route('/not-found')
    def not_found():
        return render_template('errors/not_found.html', error=True), 404

    # Rota de exemplo para gerar um código de status 500
    @app.route('/internal-error')
    def internal_error():
        # Simulando um erro interno
        error = {
            'description': 'Erro interno do servidor',
            'code': 500
        }
        return render_template('errors/error.html', error=error), 500

    CORS(app)

    return app
