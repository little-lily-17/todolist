from flask import Flask, request, jsonify

app = Flask(__name__)

items = []


@app.route('/', methods=['GET'])
def hello_world():
    return 'Welcome, this is my todo list!'

@app.route('/todo', methods=['POST'])
def create():
    items.append(request.json['data'])
    return jsonify('items', items)

@app.route('/todo', methods=['GET'])
def getall():
    return jsonify('items', items)

@app.route('/todo/<int:index>', methods=['GET'])
def get(index):
    return items[index]

@app.route('/todo/update/<int:index>/<string:word>', methods=['PUT'])
def update(index, word):
    items[index] = word
    return jsonify('items', items)

@app.route('/todo/remove/<int:index>', methods=['DELETE'])
def delete(index):
    items.pop(index)
    return jsonify('items', items)

if __name__ == '__main__':
    app.run()
