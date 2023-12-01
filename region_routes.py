from flask import Blueprint, request, jsonify, render_template
from db_test import db
region_routes = Blueprint('region', __name__)


# Описание классов в SQLAlchemy моделях
class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class CarTaxParam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    from_hp_car = db.Column(db.Integer, nullable=False)
    to_hp_car = db.Column(db.Integer, nullable=False)
    from_production_year_car = db.Column(db.Integer, nullable=False)
    to_production_year_car = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Numeric, nullable=False)


@region_routes.route('/v1/region/add', methods=['POST'])
def add_region():
    data = request.form
    region_code = data['region_code']
    name = data['name']

    if Region.query.filter_by(id=region_code).first():
        message = 'Регион с этим кодом уже существует'
    else:
        region = Region(id=region_code, name=name)
        db.session.add(region)
        db.session.commit()
        message = 'Регион успешно добавлен'
    return render_template('region-add.html', message=message)


@region_routes.route('/web/region/add', methods=['GET'])
def get_region_add():
    return render_template('region-add.html')


@region_routes.route('/v1/region/update', methods=['POST'])
def update_region():
    data = request.form
    region_code = data['region_code']
    name = data['name']

# Обновляем запись в таблице tax_param
    tax_param = CarTaxParam.query.filter_by(city_id=region_code).first()
    if tax_param:
        tax_param.region_name = name
        db.session.commit()

    region = Region.query.filter_by(id=region_code).first()
    if not region:
        message = 'Региона с таким кодом не существует'
    else:
        region.name = name
        db.session.commit()
        message = 'Регион успешно обновлен'
    return render_template('region-update.html', message=message)


@region_routes.route('/web/region/update', methods=['GET'])
def get_region_update():
    return render_template('region-update.html')


@region_routes.route('/v1/region/delete', methods=['POST'])
def delete_region():
    data = request.form
    region_code = data['region_code']

# Удаляем запись из таблицы tax_param
    tax_param = CarTaxParam.query.filter_by(city_id=region_code).first()
    if tax_param:
        db.session.delete(tax_param)
        db.session.commit()

    region = Region.query.filter_by(id=region_code).first()
    if not region:
        message = 'Региона с таким кодом не существует'
    else:
        db.session.delete(region)
        db.session.commit()
        message = 'Регион успешно удалён'

    return render_template('region-delete.html', message=message)


@region_routes.route('/web/region/delete', methods=['GET'])
def get_region_delete():
    return render_template('region-delete.html')


@region_routes.route('/web/region', methods=['GET'])
def region_list():
    regions = Region.query.all()
    return render_template('region-list.html', regions=regions)
