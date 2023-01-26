from flask import Flask
import os
from model import db
from model.user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_USER', 'admin'),
    os.getenv('DB_PASSWORD', 'password'),
    os.getenv('DB_HOST', 'localhost'),
    os.getenv('DB_PORT', '3307'),
    os.getenv('DB_NAME', 'db')
)

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run()
