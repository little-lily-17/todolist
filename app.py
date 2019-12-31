from flask import Flask, request, jsonify, json
from pymongo import MongoClient
from bson.json_util import dumps

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
    req_data['seq'] = collection.count()
    collection.insert_one(req_data)
    return "inserted"

@app.route('/todo', methods=['GET'])
def getall():
    results = []
    for x in collection.find():
        results.append(x)
    return dumps(results)


@app.route('/todo/<int:index>', methods=['GET'])
def get(index):
    return dumps(collection.find_one({"seq": index}))



@app.route('/todo/<int:index>/<string:word>', methods=['PUT'])
def update(index, word):
    collection.find_one_and_update({"seq": index},
                                 {"$set": {"data": word}})
    return dumps(collection.find_one({"seq": index}))



@app.route('/todo/<int:index>', methods=['DELETE'])
def delete(index):
    collection.delete_one({"seq": index})
    return "deleted"

if __name__ == '__main__':
    app.run()


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)