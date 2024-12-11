from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from http import HTTPStatus

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'car_service'

mysql = MySQL(app)

if __name__ == "__main__":
    app.run(debug=True)