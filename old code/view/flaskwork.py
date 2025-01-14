# from flask import Flask

# app = Flask(__name__)

# @app.route('/hello')
# def hello():
#     return 'Recieved!'

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, request

# app = Flask(__name__)

# @app.route('/receive_variable', methods=['POST'])
# def receive_variable():
#     if request.method == 'POST':
#         my_variable = request.form['myVariable']
#         # Process the received variable as needed
#         print("Received variable from PHP:", my_variable)
#         return "Variable received successfully"

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, redirect, url_for
from flask import Flask, current_app
from flask_mysqldb import MySQL
import subprocess

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flasktest'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # or your MySQL host

mysql = MySQL()
mysql.init_app(app)


#CHECK FLASDB.PY TO PRINT PORTS INTO DB and ETC

@app.route('/receive_data', methods=['POST'])
def receive_data():
    checkboxes = request.form.getlist('methods[]')
    url = request.form.getlist('url')
    FName = request.form.getlist('FName')

    #scanid = request.form.getlist(random_number)
    # Now 'checkboxes' will contain a list of selected checkboxes
    # Do whatever you need to do with this data
    print("Received checkboxes:", checkboxes,"TARGET: ",url, "SCAN ID: ",FName)

    string_to_check = "XSS"
    if string_to_check in checkboxes:
        print(f"String '{string_to_check}' exists in checkboxes")
    else:
        print(f"String '{string_to_check}' does not exist in checkboxes")    
    string_to_check1 = "ssss"
    if string_to_check1 in checkboxes:
        print(f"String '{string_to_check1}' exists in checkboxes")
    else:
        print(f"String '{string_to_check1}' does not exist in checkboxes")

    string_to_check2 = "SQL"
    if string_to_check2 in checkboxes:
        print(f"String '{string_to_check2}' exists in checkboxes")
        script_path = "./scanner/port_scanner.py"
        args = ["python3", script_path, "-t", "localhost"]
        subprocess.run(args)
        #parse_file_and_insert()

    else:
        print(f"String '{string_to_check2}' does not exist in checkboxes")


           
    
    return redirect('http://localhost:80/gradproj/scans&history/scan.php')

# Function to parse the file and insert data into the MySQL database
def parse_file_and_insert():
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("USE flasktest")  # Select the database
        with open('openedports.txt', 'r') as file:
            for line in file:
                parts = line.split()
                port = int(parts[1])
                # status = parts[2]
                print(port)
                cursor.execute("INSERT INTO ports (portID) VALUES (%s)", (port,))
                mysql.connection.commit()
        cursor.close()

# @app.route('/')
# def another_route():
#     return "Redirected successfully to another route"


if __name__ == '__main__':
    app.run(debug=True)
