from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True, type=str)
parser.add_argument('name', required=True, type=str)
parser.add_argument('address', required=True, type=str)
parser.add_argument('balance', required=True, type=int)
parser.add_argument('email', required=True, type=str)
parser.add_argument('password_hash', required=True, type=str)
