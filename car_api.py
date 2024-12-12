from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'car_service'

app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route("/get/customers", methods=["GET"])
def get_customer_records():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customers")
        rows = cur.fetchall()
        cur.close()
        
        return make_response(jsonify(rows), 200)
        
@app.route("/get/mechanics", methods=["GET"])
def get_mechanics_records():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mechanics")
    rows = cur.fetchall()
    cur.close()
    
    return make_response(jsonify(rows), 200)

if __name__ == "__main__":
    app.run(debug=True)