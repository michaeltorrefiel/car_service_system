from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from http import HTTPStatus

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'car_service'

mysql = MySQL(app)

@app.route("/customers", methods=["GET"])
def get_customer_records():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customers")
        rows = cur.fetchall()

        column_names = ["customer_id", "first_name", "last_name", "contact_number"]
        result = []
        for row in rows:
            result.append(dict(zip(column_names, row)))
        return jsonify({"success": True, "data": result, "total": len(result)}), HTTPStatus.OK
    except:
        return jsonify({"success": False, "error": "Bad Request"}), HTTPStatus.BAD_REQUEST
    finally:
        cur.close()
if __name__ == "__main__":
    app.run(debug=True)