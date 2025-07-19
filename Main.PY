from process_data import *
from flask import Flask, request

from process_data import *

app = Flask(__name__)


@app.route('/data', methods=['POST'])
def jieguo():
    data = request.get_json()
    neirong = process_data(data)
    return neirong
@app.route('/hello')
def hello():
    return "hello_world"

if __name__ == '__main__':
    app.run(debug=True)