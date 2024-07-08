from flask import Flask, render_template, request
import oracledb

app = Flask(__name__)

# Directly provide the connection string
username = "dbuser"
password = "dbuser"
dsn = "localhost:1521/xepdb1"  # E.g., "localhost:1521/orclpdb1"

def get_db_connection():
    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=dsn
    )
    return connection

@app.route('/', methods=['GET', 'POST'])
def search():
    customers = []
    column_names = []
    if request.method == 'POST':
        emailaddress = request.form.get('emailaddress')
        firstname = request.form.get('firstname')
        customerkey = request.form.get('customerkey')

        query = "SELECT * FROM customers WHERE 1=1"
        params = {}
        
        if emailaddress:
            query += " AND emailaddress LIKE :emailaddress"
            params['emailaddress'] = f"%{emailaddress}%"
        if firstname:
            query += " AND firstname LIKE :firstname"
            params['firstname'] = f"%{firstname}%"
        if customerkey:
            query += " AND customerkey LIKE :customerkey"
            params['customerkey'] = f"%{customerkey}%"

        # Debugging: Print query and params
        print(f"Query: {query}")
        print(f"Params: {params}")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            customers = cursor.fetchall()
            column_names = [col[0] for col in cursor.description]
            cursor.close()
            conn.close()
        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Database error: {error.message}")
    
    return render_template('template.html', customers=customers, column_names=column_names)

if __name__ == '__main__':
    app.run(debug=True)
