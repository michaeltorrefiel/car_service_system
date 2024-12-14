from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from datetime import datetime

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

def query_exec(query, params):
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    return(rows)

@app.route("/<table>", methods=["GET"])
def get_records(table):
    db_tables = ["customers", "mechanics", "cars", "bookings"]
    if table not in db_tables:
        return make_response(jsonify({"error": "Table not found"}), 404)

    rows = query_exec(f"select * from %s", (table,))
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

    query = f"select * from {table} where {id_type} = %s"
    rows = query_exec(query, (id,))
    if not rows:
        return make_response(jsonify({"error": "No records found"}), 404)
    
    return make_response(jsonify(rows), 200)

@app.route("/cars/<plate_number>", methods=["GET"])
def get_car_records_by_id(plate_number):
    if len(plate_number) > 9:
        return make_response(jsonify({"error": "Invalid plate number"}), 400)

    rows = query_exec("select * from cars where plate_number = %s", (plate_number,))
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

        cur.execute("insert into customers(first_name, last_name, contact_number) value (%s, %s, %s)", (first_name, last_name, contact_number))
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

        cur.execute("insert into mechanics(first_name, last_name, contact_number, other_mechanic_details) value (%s, %s, %s, %s)", (first_name, last_name, contact_number, other_mechanic_details))
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

        cur.execute("insert into cars(plate_number, customer_id, manufacturer, model, known_issue, other_details) value (%s, %s, %s, %s, %s, %s)", (plate_number, customer_id, manufacturer, model, known_issue, other_details))
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

        cur.execute("insert into bookings(mechanic_id, customer_id, plate_number, date_time_of_service, payment) value (%s, %s, %s, %s, %s)", (mechanic_id, customer_id, plate_number, date_time_of_service, payment))
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
    update_fields = []
    update_values = []
    if table == "customers":
        first_name = info.get("first_name")
        last_name = info.get("last_name")
        contact_number = info.get("contact_number")

        if first_name:
            update_fields.append("first_name = %s")
            update_values.append(first_name)
        if last_name:
            update_fields.append("last_name = %s")
            update_values.append(last_name)
        if contact_number:
            update_fields.append("contact_number = %s")
            update_values.append(contact_number)

        update_values.append(id)
        id_type = "customer_id"

    elif table == "mechanics":
        first_name = info.get("first_name")
        last_name = info.get("last_name")
        contact_number = info.get("contact_number")
        other_mechanic_details = info.get("other_mechanic_details")

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

        update_values.append(id)
        id_type = "mechanic_id"

    else:
        mechanic_id = info.get("mechanic_id")
        customer_id = info.get("customer_id")
        plate_number = info.get("plate_number")
        date_time_of_service = info.get("date_time_of_service")
        payment = info.get("payment")
        
        if mechanic_id:
            update_fields.append("mechanic_id = %s")
            update_values.append(mechanic_id)
        if customer_id:
            update_fields.append("customer_id = %s")
            update_values.append(customer_id)
        if plate_number:
            update_fields.append("plate_number = %s")
            update_values.append(plate_number)
        if date_time_of_service:
            update_fields.append("date_time_of_service = %s")
            update_values.append(date_time_of_service)
        if payment:
            update_fields.append("payment = %s")
            update_values.append(payment)

        update_values.append(id)
        id_type = "booking_id"
    
    if not update_fields:
        return make_response(jsonify({"message": "no fields provided"}), 400)
    
    cur.execute(f"update {table} set {', '.join(update_fields)} where {id_type} = %s", tuple(update_values))
    
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    if rows_affected > 0:
        return make_response(jsonify({"message": "record updated successfully", "rows_affected": rows_affected}), 200)
    else:
        return make_response(jsonify({"message": "record not found"}), 404)

@app.route("/cars/<plate_number>", methods=["PUT"])
def edit_cars_records(plate_number):
    cur = mysql.connection.cursor()

    info = request.get_json()
    customer_id = info.get("customer_id")
    manufacturer = info.get("manufacturer")
    model = info.get("model")
    known_issue = info.get("known_issue")
    other_details = info.get("other_details")

    update_fields = []
    update_values = []

    if customer_id:
        update_fields.append("customer_id = %s")
        update_values.append(customer_id)
    if manufacturer:
        update_fields.append("manufacturer = %s")
        update_values.append(manufacturer)
    if model:
        update_fields.append("model = %s")
        update_values.append(model)
    if known_issue:
        update_fields.append("known_issue = %s")
        update_values.append(known_issue)
    if other_details:
        update_fields.append("other_details = %s")
        update_values.append(other_details)

    update_values.append(plate_number)

    if not update_fields:
        return make_response(jsonify({"message": "no fields provided"}), 400)

    cur.execute(f"update cars set {', '.join(update_fields)} where plate_number = %s", tuple(update_values))

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    if rows_affected > 0:
        return make_response(jsonify({"message": "record updated successfully", "rows_affected": rows_affected}), 200)
    else:
        return make_response(jsonify({"message": "record not found"}), 404)

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

    query = f"delete from {table} where {id_type} = %s"
    cur.execute(query, (id,))

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

if __name__ == "__main__":
    app.run(debug=True)