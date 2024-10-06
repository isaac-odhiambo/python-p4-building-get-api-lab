#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    # Fetch all bakeries and serialize them to JSON
    bakeries_list = [bakery.to_dict() for bakery in Bakery.query.all()]
    response = make_response(jsonify(bakeries_list), 200)
    return response

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    # Fetch a specific bakery by ID and serialize it
    bakery = Bakery.query.get_or_404(id)
    response = make_response(jsonify(bakery.to_dict()), 200)
    return response

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    # Fetch all baked goods sorted by price in descending order
    baked_goods_list = [baked_good.to_dict() for baked_good in BakedGood.query.order_by(BakedGood.price.desc()).all()]
    response = make_response(jsonify(baked_goods_list), 200)
    return response

@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    # Fetch the most expensive baked good
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).one_or_none()
    if most_expensive:
        response = make_response(jsonify(most_expensive.to_dict()), 200)
        return response
    else:
        return make_response(jsonify({'message': 'No baked goods found'}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
