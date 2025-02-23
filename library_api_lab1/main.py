from flask import Flask

from .views import main


def handle_404(e):
    message = str(e.description) if e.description else 'Not found'
    return {'error': message}, 404


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main, url_prefix='/v1/api')
    app.register_error_handler(404, handle_404)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5050)
