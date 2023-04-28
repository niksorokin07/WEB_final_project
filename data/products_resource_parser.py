from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('price', required=True, type=int)
parser.add_argument('description', required=True, type=str)
parser.add_argument('image', required=True, type=str)
parser.add_argument('categories', required=True)
parser.add_argument('owner', required=True, type=int)
