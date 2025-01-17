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
app.config['MYSQL_DATABASE_DB'] = 'xscannerapp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # or your MySQL host

mysql = MySQL()
mysql.init_app(app)


#CHECK FLASDB.PY TO PRINT PORTS INTO DB and ETC

@app.route('/receive_data', methods=['POST'])
def receive_data():
    checkboxes = request.form.getlist('methods[]')
    url = request.form.getlist('url')
    ScanID = request.form.getlist('ScanID')
    userconID = request.form.getlist('userconID')    

    #scanid = request.form.getlist(random_number)
    # Now 'checkboxes' will contain a list of selected checkboxes
    # Do whatever you need to do with this data
    print("Received checkboxes:", checkboxes,"TARGET: ",url, "SCAN ID: ",ScanID, "User ID: ",userconID)
    insertscanid(ScanID,userconID)
    string_to_check = "XSS"
    if string_to_check in checkboxes:
        urlx = "http://"+url[0]
        print(f"String '{string_to_check}' exists in checkboxes")
        #print("url is ",url[0])
        script_path = "./scanner/pwnxss.py"
        args = ["python3", script_path, "-u", urlx, "--depth", "1"]
        subprocess.run(args)
        xss_parse_file_and_insert(ScanID,userconID)
    else:
        print(f"String '{string_to_check}' does not exist in checkboxes")    
    string_to_check1 = "SQL"
    if string_to_check1 in checkboxes:
        print(f"String '{string_to_check1}' exists in checkboxes")
        urlx = "http://"+url[0]
        print(f"String '{string_to_check}' exists in checkboxes")
        #print("url is ",url[0])
        script_path = "./scanner/sql.py"
        args = ["python3", script_path, urlx]
        subprocess.run(args)
        sql_parse_file_and_insert(ScanID,userconID)
    else:
        print(f"String '{string_to_check1}' does not exist in checkboxes")

    string_to_check2 = "PortScan"
    if string_to_check2 in checkboxes:
        print(f"String '{string_to_check2}' exists in checkboxes")
        script_path = "./scanner/port_scanner.py"
        args = ["python3", script_path, "-t", url[0]]
        subprocess.run(args)
        parse_file_and_insert(ScanID,userconID)

    else:
        print(f"String '{string_to_check2}' does not exist in checkboxes")

    string_to_check3 = "RCE"
    if string_to_check3 in checkboxes:
        print(f"String '{string_to_check3}' exists in checkboxes")
        script_path = "./scanner/s4sscanner.py"
        args = ["python3", script_path, "-u", url[0]]
        subprocess.run(args)
        #parse_file_and_insert(ScanID,userconID)

    else:
        print(f"String '{string_to_check3}' does not exist in checkboxes")
           
    
    return redirect('http://localhost:80/xscanner/template/scans&history/scan.php')

# Function to parse the file and insert data into the MySQL database
def parse_file_and_insert(ScanID,userconID):
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("USE xscannerapp")  # Select the database
        # cursor.execute("INSERT INTO scans (userID, ScanID) VALUES (%s, %s)", (userconID, ScanID))
        with open('openedports.txt', 'r') as file:
            for line in file:
                parts = line.split()
                port = int(parts[1])
                # status = parts[2]
                print(port)
                cursor.execute("INSERT INTO xports (portID, ScanID) VALUES (%s,%s)", (port,ScanID))
                mysql.connection.commit()
        cursor.close()


def xss_parse_file_and_insert(ScanID,userconID):
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("USE xscannerapp")  # Select the database
        # cursor.execute("INSERT INTO scans (userID, ScanID) VALUES (%s, %s)", (userconID, ScanID))
        with open('xss.txt', 'r') as file:
            for line in file:
                xss = line.strip()  # Remove any leading/trailing whitespace
                # status = parts[2]
                print(xss)
                cursor.execute("INSERT INTO xss (xssresult, ScanID) VALUES (%s,%s)", (xss,ScanID))
                mysql.connection.commit()
        cursor.close()       

def sql_parse_file_and_insert(ScanID,userconID):
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("USE xscannerapp")  # Select the database
        # cursor.execute("INSERT INTO scans (userID, ScanID) VALUES (%s, %s)", (userconID, ScanID))
        with open('sqlresult.txt', 'r') as file:
            for line in file:
                sqlresult = line.strip()  # Remove any leading/trailing whitespace
                # status = parts[2]
                print(sqlresult)
                cursor.execute("INSERT INTO xsql (sqlresult, ScanID) VALUES (%s,%s)", (sqlresult,ScanID))
                mysql.connection.commit()
        cursor.close()

def insertscanid(ScanID, userconID):
    with app.app_context():
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("USE xscannerapp")  # Select the database
            cursor.execute("INSERT INTO scans (userID, ScanID) VALUES (%s, %s)", (userconID, ScanID))
            
            # Commit the transaction
            mysql.connection.commit()
            
        except Exception as e:
            # Rollback the transaction in case of an error
            mysql.connection.rollback()
            print("Error:", e)
            
        finally:
            # Close the cursor
            cursor.close()

            


# @app.route('/')
# def another_route():
#     return "Redirected successfully to another route"


if __name__ == '__main__':
    app.run(debug=True)
