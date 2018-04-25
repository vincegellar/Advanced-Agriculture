from flask import Flask, request, jsonify
from werkzeug.serving import run_simple

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get2():
    return "Hello flask 2"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
