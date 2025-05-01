import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from models import db
from views import BookListResource, BookResource
from flask import Blueprint

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SWAGGER'] = {
    'title': 'Library API',
    'uiversion': 3,
    'definitions': {
        'Book': {
            'type': 'object',
            'properties': {
                'id': {
                    'type': 'integer',
                    'description': 'Book ID'
                },
                'title': {
                    'type': 'string',
                    'description': 'Title of the book'
                },
                'author': {
                    'type': 'string',
                    'description': 'Author of the book'
                },
                'year': {
                    'type': 'integer',
                    'description': 'Year of publication'
                },
                'publisher': {
                    'type': 'string',
                    'description': 'Publisher of the book'
                }
            }
        }
    }
}

db.init_app(app)

library = Blueprint('library', __name__)

swagger = Swagger(app)

library_api = Api(library)

library_api.add_resource(BookListResource, '/books')
library_api.add_resource(BookResource, '/books/<int:book_id>')

app.register_blueprint(library, url_prefix='/v1/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5050, debug=True)
