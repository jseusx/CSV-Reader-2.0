from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv

app = Flask(__name__)

def init_db():
    with sqlite3.connect('funding_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funding_information (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       serial_number TEXT NOT NULL,
                       model TEXT NOT NULL,
                       order_number TEXT,
                       funding_source TEXT
                       )
                       ''')    
        conn.commit()

# initial reading of csv file 
def import_csv_to_db(csv_file_path,db_path):
    # connect to db
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # open csv file
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            # insert data into database
            cursor.execute('''
                INSERT INTO funding_information (serial_number, model, order_number, funding_source)
                values (?, ?, ?, ?)
                ''', (row['S/N'], row['model'], row['order_number'], row['funding']))
            
        conn.commit()
        conn.close()
    print("Data imported successfully!")


# index page
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

# sends serial number to /order_number
@app.route("/submit", methods=["GET", "POST"])
def submit_serial_number():
    serial_number = request.form.get("serial_number")
    print(f"Serial Number: {serial_number}")

    return redirect(url_for('order_number', serial_number=serial_number))

# gets all info gathered and will submit it to another db and csv for user to know which serial numbers were added.
@app.route("/order_number", methods=["GET", "POST"])
def order_number():
    serial_number = request.args.get("serial_number") or request.form.get("serial_number")
    print(f"Serial Number /order_number : {serial_number}")
    if request.method == "POST":
        order_number = request.form.get("order_number")
        funding_source = get_funding_information(order_number)
        model = request.form.get("model")

        # Redirect to `add_funding` and include all necessary parameters
        if funding_source == "UNKNOWN":
            print(f"Serial Number UNKNOWN If statement: {serial_number}")
            return redirect(url_for('add_funding', serial_number=serial_number, order_number=order_number, model=model))


        return f"Order Number Submitted for Serial Number {serial_number}: {order_number}"
    return render_template("submitted.html", serial_number=serial_number)

# checks db for funding information and returns it.
def get_funding_information(order_number, db_path='funding_database.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT funding_source FROM funding_information
        WHERE order_number = ?
        LIMIT 1
        ''', (order_number,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "UNKNOWN"

# allows users to add funding info manually if none is found
@app.route("/add_funding", methods=["GET", "POST"])
def add_funding():
    serial_number = request.args.get("serial_number")
    print(f"Serial Number: {serial_number}")
    order_number = request.args.get("order_number")
    model = request.args.get("model")

    return render_template("add_funding.html", serial_number=serial_number, order_number=order_number, model=model)

# Writes to a new csv file for user to know what was added
# possibly add button to allow users to open the file they want to write to
def write_to_csv(serial_number, model, order_number, funding_source, file_path='new_info.csv'):
    with open(file_path, 'a' , newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([serial_number, model, order_number, funding_source])

# inserts new values into db
def update_db(serial_number, model, order_number, funding_soruce, file_path='funding_database.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO funding_information (serial_number, model, order_number, funding_source)
        VALUES (?, ?, ?, ?)
        ''', (serial_number, model, order_number, funding_soruce))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # initialize database with data from CSV before starting the server
    init_db()
    csv_file_path = '5_6th_gen_data.csv'
    db_path = 'funding_database.db'
    import_csv_to_db(csv_file_path, db_path)


    app.run(debug=True)