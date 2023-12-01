from flask import Blueprint, request, render_template
from region_routes import Region
from region_routes import CarTaxParam
from db_test import db
tax_param = Blueprint('tax_param', __name__)


# Добавление данных в таблицу Параметр налогообложения
@tax_param.route('/v1/car/tax-param/add', methods=['POST'])
def add_car_tax_param():
    data = request.form
    code_rate = data['code_rate']
    region_code = data['region_code']
    from_hp_car = data['from_hp_car']
    to_hp_car = data['to_hp_car']
    from_production_year_car = data['from_production_year_car']
    to_production_year_car = data['to_production_year_car']
    rate = data['rate']

    region = Region.query.filter_by(id=region_code).first()
    if not region:
        message = 'Регион не найден'
    else:
        car_tax_param = CarTaxParam.query.filter_by(id=code_rate,
                                                    city_id=region.id,
                                                    from_hp_car=from_hp_car,
                                                    to_hp_car=to_hp_car,
                                                    from_production_year_car=from_production_year_car,
                                                    to_production_year_car=to_production_year_car).first()
        if car_tax_param:
            message = 'Параметр налога на автомобиль уже существует'
        else:
            new_car_tax_param = CarTaxParam(id=code_rate,
                                            city_id=region.id,
                                            from_hp_car=from_hp_car,
                                            to_hp_car=to_hp_car,
                                            from_production_year_car=from_production_year_car,
                                            to_production_year_car=to_production_year_car,
                                            rate=rate)
            db.session.add(new_car_tax_param)
            db.session.commit()
            message = 'Параметр налога на автомобиль успешно добавлен'

    return render_template('tax-param-add.html', message=message)


@tax_param.route('/web/tax-param/add', methods=['GET'])
def get_tax_param_add():
    return render_template('tax-param-add.html')


# Обновление данных в таблицу Параметр налогообложения
@tax_param.route('/v1/car/tax-param/update', methods=['POST'])
def update_car_tax_param():
    data = request.form
    code_rate = data['code_rate']
    region_code = data['region_code']
    from_hp_car = data['from_hp_car']
    to_hp_car = data['to_hp_car']
    from_production_year_car = data['from_production_year_car']
    to_production_year_car = data['to_production_year_car']
    rate = data['rate']

    region = Region.query.filter_by(id=region_code).first()
    if not region:
        message = 'Регион не найден'
    else:
        car_tax_param = CarTaxParam.query.filter_by(id=code_rate).first()
        if not car_tax_param:
            message = 'Параметр налога на автомобиль не найден'
        else:
            existing_car_tax_param = CarTaxParam.query.filter_by(city_id=region.id,
                                                                 from_hp_car=from_hp_car,
                                                                 to_hp_car=to_hp_car,
                                                                 from_production_year_car=from_production_year_car,
                                                                 to_production_year_car=to_production_year_car).first()
            if existing_car_tax_param and existing_car_tax_param.id != code_rate:
                message = 'Параметр налога на автомобиль уже существует'
            else:
                car_tax_param.city_id = region.id
                car_tax_param.from_hp_car = from_hp_car
                car_tax_param.to_hp_car = to_hp_car
                car_tax_param.from_production_year_car = from_production_year_car
                car_tax_param.to_production_year_car = to_production_year_car
                car_tax_param.rate = rate

                db.session.add(car_tax_param)
                db.session.commit()
                db.session.rollback()

                message = 'Параметр налога на автомобиль успешно обновлен'

    return render_template('tax-param-update.html', message=message)


@tax_param.route('/web/tax-param/update', methods=['GET'])
def get_tax_param_update():
    return render_template('tax-param-update.html')


@tax_param.route('/v1/car/tax-param/delete', methods=['POST'])
def delete_car_tax_param():
    data = request.form
    code_rate = data['code_rate']

    car_tax_param = CarTaxParam.query.filter_by(id=code_rate).first()
    if not car_tax_param:
        message = 'Параметр налога на автомобиль не найден'
    else:
        db.session.delete(car_tax_param)
        db.session.commit()
        db.session.rollback()
        message = 'Параметр налога на автомобиль успешно удален'

    return render_template('tax-param-delete.html', message=message)


@tax_param.route('/web/tax-param/delete', methods=['GET'])
def get_tax_param_delete():
    return render_template('tax-param-delete.html')


@tax_param.route('/web/tax-param', methods=['GET'])
def get_tax_param_get():
    car_tax_params = CarTaxParam.query.all()
    return render_template('tax-param-list.html',  car_tax_params=car_tax_params)
