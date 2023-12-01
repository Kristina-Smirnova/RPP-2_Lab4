from flask import Blueprint, request, render_template
from region_routes import CarTaxParam
tax_route = Blueprint('tax_route', __name__)


@tax_route.route('/v1/car/tax/calc', methods=['GET', 'POST'])
def calculate_tax():
    data = request.form
    horsepower = int(data['horsepower'])
    year = int(data['year'])
    code_rate = data['code_rate']

    tax_object = CarTaxParam.query.filter_by(id=code_rate). \
        filter(CarTaxParam.from_production_year_car <= year). \
        filter(CarTaxParam.to_production_year_car >= year). \
        filter(CarTaxParam.from_hp_car <= horsepower). \
        filter(CarTaxParam.to_hp_car >= horsepower).first()

    if not tax_object:
        message = 'Объект налогообложения по заданным параметрам не найден'
    else:
        tax_rate = tax_object.rate
        tax = horsepower * tax_rate
        message = f'Налог на автомобиль с мощностью {horsepower} л.с. составит {tax} руб.'

    return render_template('index.html', message=message)


@tax_route.route('/', methods=['GET'])
def get_calculate_tax():
    return render_template('index.html')
