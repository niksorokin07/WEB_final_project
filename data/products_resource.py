from data.products import Products
from data import db_session
from flask_restful import abort, Resource
from flask import jsonify
from data.products_resource_parser import parser
from data.categories import Categories


def abort_if_job_not_found(prod_id):
    session = db_session.create_session()
    products = session.query(Products).get(prod_id)
    if not products:
        abort(404, message=f"Product {prod_id} not found")


class ProductsResource(Resource):
    def get(self, prod_id):
        abort_if_job_not_found(prod_id)
        session = db_session.create_session()
        product = session.query(Products).get(prod_id)
        return jsonify({'products': product.to_dict(
            only=("name", "price", "description", "image", "categories", "owner"))})

    def delete(self, product_id):
        abort_if_job_not_found(product_id)
        session = db_session.create_session()
        prod = session.query(Products).get(product_id)
        session.delete(prod)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, product_id):
        args = parser.parse_args()
        if not args or not all(key in args for key in
                               ["name", "price", "description", "image", "categories", "owner"]):
            return jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        prod = db_sess.query(Products).filter(Products.id == product_id).first()
        if prod is None:
            prod = Products()
            prod.id = product_id
        prod.name = args["name"]
        prod.price = args["price"]
        prod.description = args["description"]
        prod.image = args["image"]
        prod.categories = args["categories"]
        prod.owner = args["owner"]
        db_sess.add(prod)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class ProductsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        data = db_sess.query(Products).all()
        return jsonify({'jobs': [item.to_dict() for item in data]})

    def post(self):
        args = parser.parse_args()
        if not args or not all(key in args for key in
                               ["name", "price", "description", "image", "categories", "owner"]):
            return jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        prod = Products(name=args["name"], price=args["price"], description=args["description"], image=args["image"],
                        categories=args["categories"], owner=args["owner"])
        db_sess.add(prod)
        db_sess.commit()
        return jsonify({'success': 'OK'})
