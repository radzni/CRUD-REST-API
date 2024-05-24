from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="MyConnection",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
    return conn

@app.route('/employee', methods=['GET', 'POST'])
def all_employee():
    conn = db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM employee")
        all_employee = cursor.fetchall()
        conn.close()
        return jsonify(all_employee), 200
    
    if request.method == 'POST':
        new_employee = request.json
        sql = """INSERT INTO employee (id, first_name, last_name, date_of_birth, email, created_at, updated_at) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (new_employee['id'], new_employee['first_name'], new_employee['last_name'], 
                              new_employee['date_of_birth'], new_employee['email'], new_employee['created_at'], 
                              new_employee['updated_at']))
        conn.commit()
        conn.close()
        return "Created successfully", 201

@app.route('/employee/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_employee(id):
    conn = db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    employee = None

    if request.method == "GET":
        cursor.execute("SELECT * FROM employee WHERE id=%s", (id,))
        employee = cursor.fetchone()
        conn.close()
        if employee is not None:
            return jsonify(employee), 200
        else:
            return "Not Found", 404
            
    if request.method == 'PUT':
        updated_employee = request.json
        sql = """UPDATE employee SET first_name=%s, last_name=%s, date_of_birth=%s, email=%s, updated_at=%s 
                 WHERE id=%s"""
        cursor.execute(sql, (updated_employee['first_name'], updated_employee['last_name'], 
                             updated_employee['date_of_birth'], updated_employee['email'], 
                             updated_employee['updated_at'], id))
        conn.commit()
        conn.close()
        return "Updated successfully", 200

    if request.method == 'DELETE':
        sql = """DELETE FROM employee WHERE id=%s"""
        cursor.execute(sql, (id,))
        conn.commit()
        conn.close()
        return "The employee with id:{} has been deleted.".format(id), 200

if __name__ == '__main__':
    app.run(debug=True)
