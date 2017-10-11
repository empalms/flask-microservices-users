# project/api/views.py

from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

from project.api.models import User
from project import db

# instantiate users blueprint
users_blueprint = Blueprint('users', __name__, template_folder='./templates')




# routes


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Returns index HTML template"""

    # if request is POST (i.e. new user is submitted)

    if request.method == 'POST':
        # get user request
        username = request.form['username']
        email = request.form['email']
        # create new user in db
        db.session.add(User(username=username, email=email))
        db.session.commit()
    
    # handle GET - show all users
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('index.html', users=users)




@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    """Test Route."""

    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })




@users_blueprint.route('/users', methods=['POST'])
def add_user():
    """Creates new user in the users table."""

    # get JSON from post request
    post_data = request.get_json()

    # enforce input
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        return jsonify(response_object), 400

    # remember fields
    username = post_data.get('username')
    email = post_data.get('email')

    # check for duplicate users and add to db
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            reponse_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return jsonify(reponse_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, that email already exists'
            }
            return jsonify(response_object), 400

    # if missing fields
    except exc.IntegrityError as e:
        # rollback current transaction and close any subtransactions
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        return jsonify(response_object), 400




@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details"""
    
    # default error
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }

    # get user by query
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        # user doesn't exist
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at
                }
            }
            return jsonify(response_object), 200

    # invalid id
    except ValueError:
        return jsonify(response_object), 404




@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    # remember query
    users = User.query.all()

    # initalize user list
    users_list = []
    for user in users:
        user_object = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
        users_list.append(user_object)

    # success response
    response_object = {
        'status': 'success',
        'data': {
            'users': users_list
        }
    }
    return jsonify(response_object), 200
