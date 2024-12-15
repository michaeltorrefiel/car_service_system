from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from datetime import datetime
import jwt
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

app.config['SECRET_KEY'] = 'secret_key'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route('/test_db')
def test_db():
    return f"Connected to DB: {app.config['MYSQL_DB']}"

@app.route("/login", methods=["POST"])
def login():
    user = {
        "username": "michael_torrefiel",
        "password": "torrefiel321"
    }

    info = request.get_json()
    username = info.get("username")
    password = info.get("password")

    if username == user["username"] and password == user["password"]:
        token = jwt.encode({"username": username}, app.config["SECRET_KEY"], algorithm="HS256")
        return make_response(jsonify({"token": token}))
    return make_response(jsonify({"message": "Invalid username or password"}), 401)

@app.route("/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization")

    if not token:
        return make_response(jsonify({"error": "Token missing!"}), 403)

    try:
        decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return jsonify({"message": f"Welcome, {decoded['username']}!"})
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token!"}), 403

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

    query = f"select * from {table} where {id_type} = {id}"
    rows = query_exec(query)
    if not rows:
        return make_response(jsonify({"error": "No records found"}), 404)

    return make_response(jsonify(rows), 200)

@app.route("/cars/<plate_number>", methods=["GET"])
def get_car_records_by_id(plate_number):
    if len(plate_number) > 9:
        return make_response(jsonify({"error": "Invalid plate number"}), 400)

    rows = query_exec(f"select * from cars where plate_number = {plate_number}")
    if not rows:
        return make_response(jsonify({"error": "No records found"}), 404)

    return make_response(jsonify(rows), 200)

@app.route("/<table>", methods=["POST"])
def add_records(table):
    cur = mysql.connection.cursor()

    db_tables = ["customers", "mechanics", "cars", "bookings"]
    if table not in db_tables:
        return make_response(jsonify({"error": "Table not found"}), 404)

    info = request.get_json()
    if not info:
        return make_response(jsonify({"error": "Invalid JSON payload"}), 400)

    if table == "customers":
        required_fields = ["first_name", "last_name", "contact_number"]
    elif table == "mechanics":
        required_fields = ["first_name", "last_name", "contact_number"]
    elif table == "cars":
        required_fields = ["plate_number", "customer_id", "manufacturer", "model"]
    else:
        required_fields = ["mechanic_id", "customer_id", "plate_number", "date_time_of_service", "payment"]

    missing_fields = [field for field in required_fields if field not in info]
    if missing_fields:
        return make_response(jsonify({"error": "Missing fields"}), 400)

    if table == "customers":
        first_name = info["first_name"]
        last_name = info["last_name"]
        contact_number = info["contact_number"]

        if not isinstance(first_name, str) or not isinstance(last_name, str) or not isinstance(contact_number, str):
            return make_response(jsonify({"error": "Invalid input type"}), 400)

        cur.execute(f"insert into customers(first_name, last_name, contact_number) values ('{first_name}', '{last_name}', '{contact_number}')")
        record_name = "customer"
        id_type = "customer_id"
        id = cur.lastrowid


    elif table == "mechanics":
        first_name = info["first_name"]
        last_name = info["last_name"]
        contact_number = info["contact_number"]
        other_mechanic_details = info.get("other_mechanic_details", "")

        if not isinstance(first_name, str) or not isinstance(last_name, str) or not isinstance(contact_number, str):
            return make_response(jsonify({"error": "Invalid input type"}), 400)

        cur.execute(f"insert into mechanics(first_name, last_name, contact_number, other_mechanic_details) values ('{first_name}', '{last_name}', '{contact_number}', '{other_mechanic_details}')")
        record_name = "mechanic"
        id_type = "mechanic_id"
        id = cur.lastrowid


    elif table == "cars":
        plate_number = info["plate_number"]
        customer_id = info["customer_id"]
        manufacturer = info["manufacturer"]
        model = info["model"]
        known_issue = info.get("known_issue", "")
        other_details = info.get("other_details", "")

        if not isinstance(plate_number, str) or not isinstance(customer_id, int) or not isinstance(manufacturer, str) or not isinstance(model, str):
            return make_response(jsonify({"error": "Invalid input type"}), 400)

        if len(plate_number) > 9:
            return make_response(jsonify({"error": "Invalid plate number"}), 400)

        cur.execute(f"insert into cars(plate_number, customer_id, manufacturer, model, known_issue, other_details) values ('{plate_number}', '{customer_id}', '{manufacturer}', '{model}', '{known_issue}', '{other_details}')")
        record_name = "car"
        id_type = "plate_number"
        id = plate_number

    else:
        mechanic_id = info["mechanic_id"]
        customer_id = info["customer_id"]
        plate_number = info["plate_number"]
        date_time_of_service = info["date_time_of_service"]
        payment = info["payment"]

        if not isinstance(mechanic_id, int) or not isinstance(customer_id, int) or not isinstance(plate_number, str) or not isinstance(payment, str):
            return make_response(jsonify({"error": "Invalid input type"}), 400)

        try:
            datetime.strptime(date_time_of_service, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return make_response(jsonify({"error": "Invalid datetime format. Must be in yyyy-mm-dd hh:mm:ss"}), 400)

        cur.execute(f"insert into bookings(mechanic_id, customer_id, plate_number, date_time_of_service, payment) values ('{mechanic_id}', '{customer_id}', '{plate_number}', '{date_time_of_service}', '{payment}')")
        record_name = "booking"
        id_type = "booking_id"
        id = cur.lastrowid


    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": f"{record_name} added successfully", "rows_affected": rows_affected, id_type: id}), 201)

@app.route("/<table>/<int:id>", methods=["PUT"])
def edit_records_by_id(table, id):
    db_tables = ["customers", "mechanics", "bookings"]
    if table not in db_tables:
        return make_response(jsonify({"error": "Table not found"}), 404)

    cur = mysql.connection.cursor()

    info = request.get_json()
    if not info:
        return make_response(jsonify({"error": "Invalid JSON payload"}), 400)

    update_fields = []
    if table == "customers":
        first_name = info.get("first_name")
        last_name = info.get("last_name")
        contact_number = info.get("contact_number")

        if first_name:
            update_fields.append(f"first_name = '{first_name}'")
        if last_name:
            update_fields.append(f"last_name = '{last_name}'")
        if contact_number:
            update_fields.append(f"contact_number = '{contact_number}'")

        if not isinstance(first_name, str) or not isinstance(last_name, str) or not isinstance(contact_number, str):
            return make_response(jsonify({"error": "Invalid input type"}), 400)

        id_type = "customer_id"

    elif table == "mechanics":
        first_name = info.get("first_name")
        last_name = info.get("last_name")
        contact_number = info.get("contact_number")
        other_mechanic_details = info.get("other_mechanic_details")

        if first_name:
            update_fields.append(f"first_name = '{first_name}'")
        if last_name:
            update_fields.append(f"last_name = '{last_name}'")
        if contact_number:
            update_fields.append(f"contact_number = '{contact_number}'")
        if other_mechanic_details:
            update_fields.append(f"other_mechanic_details = '{other_mechanic_details}'")

        if not isinstance(first_name, str) or not isinstance(last_name, str) or not isinstance(contact_number, str):
            return make_response(jsonify({"error": "Invalid input type"}), 400)

        id_type = "mechanic_id"

    else:
        mechanic_id = info.get("mechanic_id")
        customer_id = info.get("customer_id")
        plate_number = info.get("plate_number")
        date_time_of_service = info.get("date_time_of_service")
        payment = info.get("payment")

        if mechanic_id:
            update_fields.append(f"mechanic_id = '{mechanic_id}'")
        if customer_id:
            update_fields.append(f"customer_id = '{customer_id}'")
        if plate_number:
            update_fields.append(f"plate_number = '{plate_number}'")

        if date_time_of_service:
            try:
                datetime.strptime(date_time_of_service, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return make_response(jsonify({"error": "Invalid datetime format. Must be in yyyy-mm-dd hh:mm:ss"}), 400)
            update_fields.append(f"date_time_of_service = '{date_time_of_service}'")

        if payment:
            update_fields.append(f"payment = '{payment}'")

        if not isinstance(mechanic_id, int) or not isinstance(customer_id, int) or not isinstance(plate_number, str) or not isinstance(payment, str):
            return make_response(jsonify({"error": "Invalid input type"}), 400)

        id_type = "booking_id"

    if not update_fields:
        return make_response(jsonify({"error": "no fields provided"}), 400)


    cur.execute(f"update {table} set {', '.join(update_fields)} where {id_type} = {id}")

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    if rows_affected > 0:
        return make_response(jsonify({"message": "record updated successfully", "rows_affected": rows_affected}), 200)
    else:
        return make_response(jsonify({"error": "record not found"}), 404)

@app.route("/cars/<plate_number>", methods=["PUT"])
def edit_cars_records(plate_number):
    cur = mysql.connection.cursor()

    info = request.get_json()
    if not info:
        return make_response(jsonify({"error": "Invalid JSON payload"}), 400)

    customer_id = info.get("customer_id")
    manufacturer = info.get("manufacturer")
    model = info.get("model")
    known_issue = info.get("known_issue")
    other_details = info.get("other_details")

    update_fields = []

    if customer_id:
        update_fields.append(f"customer_id = '{customer_id}'")
    if manufacturer:
        update_fields.append(f"manufacturer = '{manufacturer}'")
    if model:
        update_fields.append(f"model = '{model}'")
    if known_issue:
        update_fields.append(f"known_issue = '{known_issue}'")
    if other_details:
        update_fields.append(f"other_details = '{other_details}'")

    if not update_fields:
        return make_response(jsonify({"error": "no fields provided"}), 400)

    if not isinstance(plate_number, str) or not isinstance(customer_id, int) or not isinstance(manufacturer, str) or not isinstance(model, str):
        return make_response(jsonify({"error": "Invalid input type"}), 400)

    if len(plate_number) > 9:
        return make_response(jsonify({"error": "Invalid plate number"}), 400)


    cur.execute(f"update cars set {', '.join(update_fields)} where plate_number = {plate_number}")

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    if rows_affected > 0:
        return make_response(jsonify({"message": "record updated successfully", "rows_affected": rows_affected}), 200)
    else:
        return make_response(jsonify({"error": "record not found"}), 404)

@app.route("/<table>/<int:id>", methods=["DELETE"])
def delete_records_by_id(table, id):
    db_tables = ["customers", "mechanics", "bookings"]
    if table not in db_tables:
        return make_response(jsonify({"error": "Table not found"}), 404)

    cur = mysql.connection.cursor()

    if table == "customers":
        id_type = "customer_id"

    elif table == "mechanics":
        id_type = "mechanic_id"

    else:
        id_type = "booking_id"

    query = f"delete from {table} where {id_type} = {id}"
    cur.execute(query)

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    if rows_affected > 0:
        return make_response(jsonify({"message": "record deleted successfully", "rows_affected": rows_affected}), 200)
    else:
        return make_response(jsonify({"error": "record not found"}), 404)

@app.route("/cars/<plate_number>", methods = ["DELETE"])
def delete_car_records(plate_number):
    cur = mysql.connection.cursor()

    cur.execute(f"delete from cars where plate_number = {plate_number}")

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    if rows_affected > 0:
        return make_response(jsonify({"message": "record deleted successfully", "rows_affected": rows_affected}), 200)
    else:
        return make_response(jsonify({"error": "record not found"}), 404)

@app.route("/mechanics/schedule/<int:id>", methods=["GET"])
def get_mechanic_bookings(id):
    query = f"""
    select concat(m.first_name, " ", m.last_name) full_name, b.date_time_of_service sched from mechanics m left join bookings b on m.mechanic_id = b.mechanic_id where m.mechanic_id = {id};
    """
    rows = query_exec(query)

    if not rows:
        return make_response(jsonify({"error": "No records found"}), 404)

    return make_response(jsonify(rows), 200)

@app.route("/cars/details/<plate_number>", methods=["GET"])
def get_car_details(plate_number):
    query = f"select plate_number, manufacturer, model from cars where plate_number = {plate_number}"

    rows = query_exec(query)

    if not rows:
        return make_response(jsonify({"error": "No records found"}), 404)

    return make_response(jsonify(rows), 200)

@app.route("/customers/bills/<int:id>", methods=["GET"])
def get_customer_bills(id):
    query = f"""
    select concat(c.first_name, " ", c.last_name) full_name, b.plate_number, b.payment from customers c left join bookings b on c.customer_id = b.customer_id where c.customer_id = {id};
    """
    rows = query_exec(query)

    if not rows:
        return make_response(jsonify({"error": "No records found"}), 404)

    return make_response(jsonify(rows), 200)

if __name__ == "__main__":
    app.run(debug=True)