from flask import Flask
from region_routes import region_routes
from tax_param_route import tax_param
from tax_route import tax_route
from db_test import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/RPP_Lab4'
app.register_blueprint(region_routes)
app.register_blueprint(tax_param)
app.register_blueprint(tax_route)

app.config['SQLAlchemy_TRACK_MODIFIVATTION'] = False
db.init_app(app)


# Обработчик запроса на файл favicon.ico
@app.route('/favicon.ico')
def favicon():
    return ''


if __name__ == '__main__':
    app.run(debug=True)
