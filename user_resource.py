from data.users import User
from data import db_session
from flask_restful import abort, Resource
from flask import jsonify
from werkzeug.security import generate_password_hash
from data.user_resource_parser import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"News {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        data = db_sess.query(User).get(user_id)
        if not data:
            return jsonify({'error': 'Not found'})
        return jsonify({
            'user': data.to_dict(
                only=('email', 'password_hash', 'surname', 'name', 'age', 'position', 'speciality', 'address'))
        })

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        el = db_sess.query(User).get(user_id)
        if not el:
            return jsonify({'error': 'Bad request'})
        db_sess.delete(el)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = parser.parse_args()
        if not args or not all(key in args for key in
                               ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                                'password_hash', 'modified_date', ]):
            return jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if user is None:
            user = User()
            user.id = user_id
        user.surname = args['surname'],
        user.name = args['name'],
        user.age = args['age'],
        user.position = args['position'],
        user.speciality = args['speciality'],
        user.address = args['address'],
        user.email = args['email'],
        user.password_hash = generate_password_hash(args['password_hash']),
        user.modified_date = args['modified_date'],
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        data = db_sess.query(User).all()
        return jsonify({'users': [item.to_dict() for item in data]})

    def post(self):
        args = parser.parse_args()
        if not args or not all(key in args for key in
                               ['address', 'age', 'email', 'modified_date', 'name', 'position', 'surname',
                                'speciality', 'password_hash']):
            return jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            password_hash=generate_password_hash(args['password_hash']),
            modified_date=args['modified_date'],
        )
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})
