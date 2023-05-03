import flask
from flask import jsonify, request
from data import db_session
from data.users import User
from werkzeug.security import generate_password_hash

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('name', 'surname', 'email'))
                 for item in db_sess.query(User).all()]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == user_id).first()
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': users.to_dict(only=('surname', 'name', 'email'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['email', 'password_hash', 'surname', 'name', 'balance', 'address']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if "id" in request.json:
        if db_sess.query(User).filter(request.json["id"] == User.id).first():
            return jsonify({'error': "Id already exists"})
    args = request.json
    user = User()
    user.id = args["id"]
    user.surname = args['surname']
    user.name = args['name']
    user.balance = args['balance']
    user.address = args['address']
    user.email = args['email']
    user.password_hash = generate_password_hash(args['password_hash'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    db_sess = db_session.create_session()
    el = db_sess.query(User).filter(User.id == id).first()
    if not el:
        return jsonify({'error': 'Bad request'})
    db_sess.delete(el)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:id>', methods=['PUT'])
def edit_user(id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['email', 'password_hash', 'surname', 'name', 'balance', 'address']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if not user:
        return jsonify({'error': "Id doesn't exist"})
    args = request.json
    user.surname = args['surname']
    user.name = args['name']
    user.balance = args['balance']
    user.address = args['address']
    user.email = args['email']
    user.password_hash = generate_password_hash(args['password_hash'])
    db_sess.commit()
    return jsonify({'success': 'OK'})
