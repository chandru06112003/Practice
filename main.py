from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)
# Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}, email: {self.email}>'

user_arg = reqparse.RequestParser()
user_arg.add_argument('username', type=str, required=True, help='Username cannot be blank')
user_arg.add_argument('email', type=str, required=True, help='Email cannot be blank')

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users
    
    # @marshal_with(user_fields)
    # def post(self):
    #     args = user_arg.parse_args()
    #     new_user = User(username=args['username'], email=args['email'])
    #     db.session.add(new_user)
    #     db.session.commit()
    #     users = User.query.all()
    #     return users, 201
    
class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    @marshal_with(user_fields)
    def patch(self, user_id):
        args = user_arg.parse_args()
        user = User.query.get_or_404(user_id)
        if 'username' in args:
            user.username = args['username']
            user.email = args['email']
        db.session.commit()
        return user
    @marshal_with(user_fields)
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        users = User.query.all()
        return users
    
api.add_resource(Users, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')    


@app.route('/')
def hello_world():
    return 'Hi'
# @app.route('/api/')
# def api_root():
#     return 

if __name__ == '__main__':
    app.run(debug=True)
