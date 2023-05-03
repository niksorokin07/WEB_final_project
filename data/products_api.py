import flask
from flask import jsonify, request
from data import db_session
from data.users import User
from data.products import Products

blueprint = flask.Blueprint(
    'products_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/products')
def get_products():
    db_sess = db_session.create_session()
    return jsonify(
        {
            'products':
                [item.to_dict(only=('name', 'owner.name'))
                 for item in db_sess.query(Products).all()]
        }
    )


@blueprint.route('/api/products/<int:prod_id>', methods=['GET'])
def get_one_product(prod_id):
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.id == prod_id).first()
    if not products:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'product': products.to_dict(only=('name', 'owner.email'))
        }
    )


@blueprint.route('/api/products', methods=['POST'])
def create_product():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["name", "price", "description", "image", "categories", "owner"]):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if "id" in request.json:
        if db_sess.query(Products).filter(request.json["id"] == Products.id).first():
            return jsonify({'error': "Id already exists"})
    args = request.json
    prod = Products()
    prod.name = args["name"]
    prod.price = args["price"]
    prod.description = args["description"]
    prod.image = args["image"]
    prod.categories = args["categories"]
    prod.owner = args["owner"]
    db_sess.add(prod)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    db_sess = db_session.create_session()
    el = db_sess.query(Products).filter(Products.id == id).first()
    if not el:
        return jsonify({'error': 'Bad request'})
    db_sess.delete(el)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/products/<int:id>', methods=['PUT'])
def edit_product(id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["name", "price", "description", "image", "categories", "owner"]):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    prod = db_sess.query(Products).get(id)
    if not prod:
        return jsonify({'error': "Id doesn't exist"})
    if not db_sess.query(User).filter(User.id == request.json['owner']).first():
        return jsonify({'error': 'Bad request'})
    args = request.json
    prod.name = args["name"]
    prod.price = args["price"]
    prod.description = args["description"]
    prod.image = args["image"]
    prod.categories = args["categories"]
    prod.owner = args["owner"]
    db_sess.commit()
    return jsonify({'success': 'OK'})
