from flask import Flask, render_template, request, url_for
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



@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        serial_number = request.form.get("serial_number")
        # Add logic to process serial number


        return f"Serial Number Submitted: {serial_number}"
    return render_template("index.html")

if __name__ == "__main__":
    # initialize database with data from CSV before starting the server
    init_db()
    csv_file_path = '5_6th_gen_data.csv'
    db_path = 'funding_database.db'
    import_csv_to_db(csv_file_path, db_path)


    app.run(debug=True)