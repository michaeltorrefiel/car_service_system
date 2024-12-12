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

@app.route("/<table>", methods=["GET"])
def get_records(table):
    db_tables = ["customers", "mechanics", "cars", "bookings"]
    if table not in db_tables:
        return make_response(jsonify({"error": "Table not found"}), 404)

    rows = query_exec(f"select * from {table}")
    if not rows:
        return make_response(jsonify({"error": "No records found"}), 404)
    
    return make_response(jsonify(rows), 200)

@app.route("/customers", methods=["POST"])
def add_customer_records():
    cur = mysql.connection.cursor()

    info = request.get_json()
    first_name = info["first_name"]
    last_name = info["last_name"]
    contact_number = info["contact_number"]
    cur.execute("insert into customers(first_name, last_name, contact_number) value (%s, %s, %s)", (first_name, last_name, contact_number))

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "customer added successfully", "rows_affected": rows_affected}), 201)

@app.route("/mechanics", methods=["POST"])
def add_mechanic_records():
    cur = mysql.connection.cursor()

    info = request.get_json()
    first_name = info["first_name"]
    last_name = info["last_name"]
    contact_number = info["contact_number"]
    other_mechanic_details = info.get("other_mechanic_details", "")
    cur.execute("insert into mechanics(first_name, last_name, contact_number, other_mechanic_details) value (%s, %s, %s, %s)", (first_name, last_name, contact_number, other_mechanic_details))

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "mechanic added successfully", "rows_affected": rows_affected}), 201)

@app.route("/cars", methods=["POST"])
def add_car_records():
    cur = mysql.connection.cursor()

    info = request.get_json()
    plate_number = info["plate_number"]
    customer_id = info["customer_id"]
    manufacturer = info["manufacturer"]
    model = info["model"]
    known_issue = info.get("known_issue", "")
    other_details = info.get("other_details", "")
    cur.execute("insert into cars(plate_number, customer_id, manufacturer, model, known_issue, other_details) value (%s, %s, %s, %s, %s, %s)", (plate_number, customer_id, manufacturer, model, known_issue, other_details))

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "car added successfully", "rows_affected": rows_affected}), 201)

@app.route("/bookings", methods=["POST"])
def add_booking_records():
    cur = mysql.connection.cursor()

    info = request.get_json()
    mechanic_id = info["mechanic_id"]
    customer_id = info["customer_id"]
    plate_number = info["plate_number"]
    date_time_of_service = info["date_time_of_service"]
    payment = info["payment"]

    cur.execute("insert into bookings(mechanic_id, customer_id, plate_number, date_time_of_service, payment) value (%s, %s, %s, %s, %s)", (mechanic_id, customer_id, plate_number, date_time_of_service, payment))

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "booking added successfully", "rows_affected": rows_affected}), 201)


@app.route("/bookings/<int:booking_id>", methods = ["DELETE"])
def delete_customer_records(booking_id):
    cur = mysql.connection.cursor()
    cur.execute("delete from bookings where booking_id = %s", (booking_id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "record deleted successfully", "rows_affected": rows_affected}), 200)

if __name__ == "__main__":
    app.run(debug=True)