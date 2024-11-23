# Description: This file contains the code for the Flask application that will be used to create the API for the e-commerce system. 
# The application will have routes to create and retrieve users, products, and orders. The application will use SQLAlchemy 
# to interact with the MySQL database and Marshmallow to serialize and deserialize the data.

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Ethan17$@localhost/e_commerce_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

# Models: one-to-many relationship between User and Order models.
class User(db.Model):# User model
    __tablename__ = "users"# Table name
    id = db.Column(db.Integer, primary_key=True)# Primary key
    name = db.Column(db.String(50), nullable=False)# Name 50 characters max.
    email = db.Column(db.String(100), unique=True, nullable=False)# Unique email 100 characters max.

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)# Name 100 characters max.
    price = db.Column(db.Float, nullable=False)# Price float integer.
    stock = db.Column(db.Integer, nullable=False)# Stock integer.
    
# Order model: many-to-one relationship with User model.
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)# Foreign key to users table.
    total_price = db.Column(db.Float, nullable=False)
    user = db.relationship("User", backref="orders")

# Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Routes
@app.route('/api/users', methods=['POST'])# POST a new user
def create_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user), 201

@app.route('/api/users', methods=['GET']) # GET all users
def get_users():
    users = User.query.all()
    return users_schema.dump(users), 200

@app.route('/api/products', methods=['POST'])# POST a new product
def create_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'], stock=data['stock'])
    db.session.add(new_product)
    db.session.commit()
    return product_schema.dump(new_product), 201

@app.route('/api/products', methods=['GET'])# GET all products
def get_products():
    products = Product.query.all()
    return products_schema.dump(products), 200

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    new_order = Order(user_id=data['user_id'], total_price=data['total_price'])
    db.session.add(new_order)
    db.session.commit()
    return order_schema.dump(new_order), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return orders_schema.dump(orders), 200

# Run server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
