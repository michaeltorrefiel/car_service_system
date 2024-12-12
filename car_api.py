from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'car_service'

app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def home_page():
    home = """
    <h1>CAR SERVICE SYSTEM</h1>
    <p>tables = ["customers", "mechanics", "cars", "bookings"] </p>
    """
    return home

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

@app.route("/<table>/<int:id>", methods=["GET"])
def get_records_by_id(table, id):
    db_tables = ["customers", "mechanics", "bookings"]
    if table not in db_tables:
        return make_response(jsonify({"error": "Table not found"}), 404)

    if table == "customers":
        id_type = "customer_id"
    elif table == "mechanics":
        id_type = "mechanic_id"
    else:
        id_type = "booking_id"
    rows = query_exec(f"select * from {table} where {id_type}= {id}")
    if not rows:
        return make_response(jsonify({"error": "No records found"}), 404)
    
    return make_response(jsonify(rows), 200)

@app.route("/cars/<plate_number>", methods=["GET"])
def get_car_records_by_id(plate_number):
    cur = mysql.connection.cursor()

    cur.execute("select * from cars where plate_number = %s", (plate_number,))
    rows = cur.fetchall()
    cur.close()
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
    customer_id = cur.lastrowid
    cur.close()

    return make_response(jsonify({"message": "customer added successfully", "rows_affected": rows_affected, "customer_id": customer_id}), 201)

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
    mechanic_id = cur.lastrowid
    cur.close()

    return make_response(jsonify({"message": "mechanic added successfully", "rows_affected": rows_affected, "mechanic_id": mechanic_id}), 201)

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

    return make_response(jsonify({"message": "car added successfully", "rows_affected": rows_affected, "plate_number": plate_number}), 201)

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
    booking_id = cur.lastrowid
    cur.close()

    return make_response(jsonify({"message": "booking added successfully", "rows_affected": rows_affected, "booking_id": booking_id}), 201)

@app.route("/customers/<int:customer_id>", methods = ["PUT"])
def edit_customer_records(customer_id):
    cur = mysql.connection.cursor()

    info = request.get_json()
    first_name = info.get("first_name")
    last_name = info.get("last_name")
    contact_number = info.get("contact_number")

    update_fields = []
    update_values = []

    if first_name:
        update_fields.append("first_name = %s")
        update_values.append(first_name)
    if last_name:
        update_fields.append("last_name = %s")
        update_values.append(last_name)
    if contact_number:
        update_fields.append("contact_number = %s")
        update_values.append(contact_number)

    update_values.append(customer_id)

    if not update_fields:
        return make_response(jsonify({"message": "no fields provided"}), 400)

    cur.execute(f"update customers set {', '.join(update_fields)} where customer_id = %s", tuple(update_values))

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    if rows_affected > 0:
        return make_response(jsonify({"message": "record updated successfully", "rows_affected": rows_affected}), 200)
    else:
        return make_response(jsonify({"message": "record not found"}), 404)

@app.route("/mechanics/<int:mechanic_id>", methods = ["PUT"])
def edit_mechanic_records(mechanic_id):
    cur = mysql.connection.cursor()

    info = request.get_json()
    first_name = info.get("first_name")
    last_name = info.get("last_name")
    contact_number = info.get("contact_number")
    other_mechanic_details = info.get("other_mechanic_details")

    update_fields = []
    update_values = []

    if first_name:
        update_fields.append("first_name = %s")
        update_values.append(first_name)
    if last_name:
        update_fields.append("last_name = %s")
        update_values.append(last_name)
    if contact_number:
        update_fields.append("contact_number = %s")
        update_values.append(contact_number)
    if other_mechanic_details:
        update_fields.append("other_mechanic_details = %s")
        update_values.append(other_mechanic_details)

    update_values.append(mechanic_id)

    if not update_fields:
        return make_response(jsonify({"message": "no fields provided"}), 400)

    cur.execute(f"update mechanics set {', '.join(update_fields)} where mechanic_id = %s", tuple(update_values))

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    if rows_affected > 0:
        return make_response(jsonify({"message": "record updated successfully", "rows_affected": rows_affected}), 200)
    else:
        return make_response(jsonify({"message": "record not found"}), 404)

@app.route("/customers/<int:customer_id>", methods = ["DELETE"])
def delete_customer_records(customer_id):
    cur = mysql.connection.cursor()

    cur.execute("delete from customers where customer_id = %s", (customer_id,))

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "record deleted successfully", "rows_affected": rows_affected}), 200)

@app.route("/mechanics/<int:mechanic_id>", methods = ["DELETE"])
def delete_mechanic_records(mechanic_id):
    cur = mysql.connection.cursor()

    cur.execute("delete from mechanics where mechanic_id = %s", (mechanic_id,))

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "record deleted successfully", "rows_affected": rows_affected}), 200)

@app.route("/cars/<plate_number>", methods = ["DELETE"])
def delete_car_records(plate_number):
    cur = mysql.connection.cursor()

    cur.execute("delete from cars where plate_number = %s", (plate_number,))
    
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "record deleted successfully", "rows_affected": rows_affected}), 200)

@app.route("/bookings/<int:booking_id>", methods = ["DELETE"])
def delete_booking_records(booking_id):
    cur = mysql.connection.cursor()

    cur.execute("delete from bookings where booking_id = %s", (booking_id,))

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "record deleted successfully", "rows_affected": rows_affected}), 200)

if __name__ == "__main__":
    app.run(debug=True)