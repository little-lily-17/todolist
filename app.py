from flask import Flask, request, jsonify, json
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['to-do-list']
collection = db['to-do-list']

items = []


@app.route('/', methods=['GET'])
def hello_world():
    return 'Welcome, this is my todo list!'


@app.route('/todo', methods=['POST'])
def create():
    items.append(request.json['data']) #will be deleted later
    req_data = request.get_json()
    collection.insert_one(req_data).inserted_id
    return "204"

@app.route('/todo', methods=['GET'])
def getall():
    return jsonify('items', items)


@app.route('/todo/<int:index>', methods=['GET'])
def get(index):
    return items[index]


@app.route('/todo/<int:index>/<string:word>', methods=['PUT'])
def update(index, word):
    items[index] = word
    return jsonify('items', items)


@app.route('/todo/<int:index>', methods=['DELETE'])
def delete(index):
    items.pop(index)
    return jsonify('items', items)

if __name__ == '__main__':
    app.run()
