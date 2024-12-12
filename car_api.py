from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'car_service'

app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

def query_exec(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return(rows)

# @app.route("/api/customers", methods=["GET"])
# def get_customer_records():
#     rows = query_exec("select * from customers")
#     return make_response(jsonify(rows), 200)
        
# @app.route("/api/mechanics", methods=["GET"])
# def get_mechanic_records():
#     rows = query_exec("select * from mechanics")
#     return make_response(jsonify(rows), 200)

# @app.route("/api/cars", methods=["GET"])
# def get_car_records():
#     rows = query_exec("select * from cars")
#     return make_response(jsonify(rows), 200)

# @app.route("/api/bookings", methods=["GET"])
# def get_booking_records():
#     rows = query_exec("select * from bookings")
#     return make_response(jsonify(rows), 200)

@app.route("/api/<table>", methods=["GET"])
def get_records(table):
    rows = query_exec(f"select * from {table}")
    return make_response(jsonify(rows), 200)

if __name__ == "__main__":
    app.run(debug=True)