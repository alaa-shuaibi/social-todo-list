import database as db
from flask import Flask, render_template, request, jsonify
from bson import json_util

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html'), 200

@app.route('/signup', methods=['POST'])
def signup():
    creds = request.json

    if creds['password'] == '':
        return jsonify({'error': 'Invalid password.'}), 400

    db_response = db.createUser(creds['username'], creds['password'])
    return jsonify(json_util.loads(json_util.dumps(db_response))), 200

@app.route('/login', methods=['POST'])
def login():
    creds = request.json
    db_response = db.login(creds['username'], creds['password'])
    
    if 'error' in db_response:
        if db_response['error'] == 'Incorrect password.':
            return jsonify(db_response), 401
        elif db_response['error'] == 'Could not find user.':
            return jsonify(db_response), 404
    
    return jsonify(db_response), 200

@app.route('/updateAccount', methods=['PUT'])
def updateProfile():
    data = request.json
    db_response = db.updateUserData(data['username'], data)

    if 'error' in db_response:
        return jsonify(db_response), 404
     
    return jsonify(db_response), 200

@app.route('/deleteAccount', methods=['DELETE'])
def deleteUser():
    data = request.json
    db_response = db.deleteUser(data['username'], data['password'])

    if 'error' in db_response:
        return jsonify(db_response), 404
    
    return jsonify(db_response), 200

@app.route('/addFriend', methods=['POST'])
def addFriend():
    data = request.json
    db_response = db.addFriend(data['username'], data['friend_username'])
    return jsonify(db_response), 200

@app.route('/removeFriend', methods=['DELETE'])
def deleteFriend():
    data = request.json
    db_response = db.removeFriend(data['username'], data['friend_username'])
    return jsonify(db_response), 200

@app.route('/addTask', methods=['POST'])
def addTask():
    data = request.json
    db_response = db.addTask(data['username'], data)
    return jsonify(db_response), 200

@app.route('/getAllTasks')
def getAllTasks():
    data = request.json
    db_response = db.getAllTasks(data['username'])
    return jsonify(db_response), 200

@app.route('/updateTask', methods=['PUT'])
def updateTask():
    data = request.json
    db_response = db.updateTask(data['username'], data)
    return jsonify(db_response), 200

@app.route('/deleteTask', methods=['DELETE'])
def deleteTask():
    data = request.json
    db_response = db.deleteTask(data['username'], data['task_id'])
    return jsonify(db_response), 200

if __name__ == '__main__':
    app.run()