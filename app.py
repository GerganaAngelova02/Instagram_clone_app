from flask import Flask
from view.user import index

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', view_func=index)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()