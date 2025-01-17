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

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    checkboxes = request.form.getlist('methods[]')
    url = request.form.getlist('url')
   # scanid = request.form.getlist(random_number)
    # Now 'checkboxes' will contain a list of selected checkboxes
    # Do whatever you need to do with this data
    print("Received checkboxes:", checkboxes,"TARGET: ",url)
    return redirect('http://localhost:80/gradproj/scans&history/scan.php')

# @app.route('/')
# def another_route():
#     return "Redirected successfully to another route"


if __name__ == '__main__':
    app.run(debug=True)
