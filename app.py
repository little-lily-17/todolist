from bson.json_util import dumps
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['to-do-list']
collection = db['to-do-list']


@app.route('/', methods=['GET'])
def hello_world():
    return 'Welcome, this is my todo list!'


@app.route('/todo', methods=['POST'])
def create():
    req_data = request.get_json()
    req_data['seq'] = collection.count()
    collection.insert_one(req_data)
    return "inserted"


@app.route('/todo', methods=['GET'])
def getall():
    results = []
    for x in collection.find({}, {'_id': 0}):
        results.append(x)
    return dumps(results)


@app.route('/todo/<int:index>', methods=['GET'])
def get(index):
    return dumps(collection.find_one({"seq": index}, {'_id': 0}))


@app.route('/todo/<int:index>', methods=['PUT'])
def update(index):
    word = request.get_json()
    collection.find_one_and_update({"seq": index}, {"$set": {"data": word}})
    return dumps(collection.find_one({"seq": index}))


@app.route('/todo/<int:index>', methods=['DELETE'])
def delete(index):
    collection.delete_one({"seq": index})
    return "deleted"


if __name__ == '__main__':
    app.run()
