# Python module imports
import datetime as dt
import hashlib
from flask import Flask, request, render_template, Response

# Importing local functions
from block import *
from genesis import create_genesis_block
from newBlock import next_block, add_block
from getBlock import find_records, find_student_records_dates, find_student_records_courses, find_student_records_comp
from checkChain import check_integrity
import pickle

# Flask declarations
app = Flask(__name__)
response = Response()
response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')

# Initializing blockchain with the genesis block
try:
        with open('blockchain.pickle', 'rb') as f:
                blockchain = pickle.load(f)
except:
        blockchain = create_genesis_block()

def write_pickle():
        global blockchain
        with open('blockchain.pickle', 'wb') as f:
                pickle.dump(blockchain, f)

data = []

# Default Landing page of the app
@app.route('/',  methods = ['GET'])
def landing():
    return render_template("landing.html")

@app.route('/index.html', methods = ['GET'])
def index():
    return render_template("index.html")

@app.route('/student_landing.html', methods = ['GET'])
def student_landing():
    return render_template("student_landing.html")

@app.route('/student_check_dates.html', methods = ['GET'])
def student_check_dates():
    return render_template("student_check_dates.html")

@app.route('/student_check_courses.html', methods = ['GET'])
def student_check_courses():
    return render_template("student_check_courses.html")

@app.route('/student_check_comp.html', methods = ['GET'])
def student_check_comp():
    return render_template("student_check_comp.html")

@app.route('/student_check_dates.html', methods = ['POST'])
def parse_student_request_dates():
    data = []
    data = find_student_records_dates(request.form, blockchain)
    if data == -1:
        return "Records not found"
    return render_template("view_students_dates.html",
                            name = request.form.get("name"),
                            number = int(request.form.get("number")),
                            date = request.form.get("date"),
                            status = data,
                            num_records = len(data))

@app.route('/student_check_courses.html', methods = ['POST'])
def parse_student_request_courses():
    data = []
    data = find_student_records_courses(request.form, blockchain)
    if data == -1:
        return "Records not found"
    return render_template("view_students_courses.html",
                            name = request.form.get("name"),
                            number = int(request.form.get("number")),
                            course = request.form.get("course"),
                            status = data,
                            num_records = len(data))

@app.route('/student_check_comp.html', methods = ['POST'])
def parse_student_request_comp():
    data = []
    data = find_student_records_comp(request.form, blockchain)
    if data == -1:
        return "Records not found"
    return render_template("view_students_comp.html",
                            name = request.form.get("name"),
                            number = int(request.form.get("number")),
                            status = data,
                            num_records = len(data))

# Get Form input and decide what is to be done with it
@app.route('/', methods = ['POST'])
def parse_request():
    if(request.form.get("name")):
        while len(data) > 0:
            data.pop()
        data.append(request.form.get("name"))
        data.append(str(dt.date.today()))
        return render_template("class.html",
                                name = request.form.get("name"),
                                date = dt.date.today())

    elif(request.form.get("number")):
        while len(data) > 2:
            data.pop()
        data.append(request.form.get("course"))
        data.append(request.form.get("year"))
        return render_template("attendance.html",
                                name = data[0],
                                course = request.form.get("course"),
                                year = request.form.get("year"),
                                number = int(request.form.get("number")))
    elif(request.form.get("roll_no1")):
        while len(data) > 4:
            data.pop()
        write_pickle()
        return render_template("result.html", result = add_block(request.form, data, blockchain))

    else:
        return "Invalid POST request. This incident has been recorded."

# Show page to get information for fetching records
@app.route('/view.html',  methods = ['GET'])
def view():
    return render_template("class.html")

# Process form input for fetching records from the blockchain
@app.route('/view.html',  methods = ['POST'])
def show_records():
    write_pickle()
    data = []
    data = find_records(request.form, blockchain)
    if data == -1:
        return "Records not found"
    return render_template("view.html",
                            name = request.form.get("name"),
                            course = request.form.get("course"),
                            year = request.form.get("year"),
                            status = data,
                            number = int(request.form.get("number")),
                            date = request.form.get("date"))

# Show page with result of checking blockchain integrity
@app.route('/result.html',  methods = ['GET'])
def check():
    write_pickle()
    return render_template("result.html", result = check_integrity(blockchain))

# Start the flask app when program is executed
if __name__ == "__main__":
    app.run()
