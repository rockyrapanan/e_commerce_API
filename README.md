# e_commerce_API
Setup Instructions

1. Clone the Repository

git clone https://github.com/your-username/ecommerce-api.git
cd ecommerce-api

2. Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate # On macOS/Linux
venv\Scripts\activate # On Windows

3. Install Dependencies

pip install -r requirements.txt

4. Configure MySQL Database

   Log in to your MySQL server and create a database:

CREATE DATABASE e_commerce_db;

Update the SQLALCHEMY_DATABASE_URI in app.py with your database credentials:

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/e_commerce_db'

5. Initialize the Database

Run the following command to create the tables:

python app.py

API Endpoints
Users
HTTP Method Endpoint Description Request Body
POST /api/users Create a new user {"name": "John", "email": "john@example.com"}
GET /api/users Retrieve all users None
Products
HTTP Method Endpoint Description Request Body
POST /api/products Add a new product {"name": "Laptop", "price": 1500.0, "stock": 10}
GET /api/products Retrieve all products None
Orders
HTTP Method Endpoint Description Request Body
POST /api/orders Create a new order {"user_id": 1, "total_price": 1500.0}
GET /api/orders Retrieve all orders None
Example Usage
Using Postman

    Start the Flask application:

    python app.py

    Open Postman and test the endpoints:
        POST /api/users to create a user.
        GET /api/users to retrieve all users.
        POST /api/products to add a product.
        GET /api/products to retrieve all products.
        POST /api/orders to create an order.
        GET /api/orders to retrieve all orders.

Using cURL

Example of creating a user:

curl -X POST http://127.0.0.1:5000/api/users \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "email": "john@example.com"}'
