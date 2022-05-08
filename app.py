from flask import Flask, render_template, request, jsonify
import database as db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html'), 200

@app.route('/signup', methods=['POST'])
def signup():
    creds = request.json
    db_response = db.createUser(creds['username'], creds['password'])
    return jsonify(db_response), 200

@app.route('/login')
def login():
    creds = request.json
    db_response = db.login(creds['username'], creds['password'])
    
    if 'error' in db_response:
        if db_response['error'] == 'Incorrect password.':
            return jsonify(db_response), 401
        elif db_response['error'] == 'Could not find user.':
            return jsonify(db_response), 404
    
    return jsonify(db_response), 200

@app.route('/updateProfile', methods=['PUT'])
def updateProfile():
    return jsonify({}), 200

@app.route('/deleteProfile', methods=['DELETE'])
def deleteUser():
    return jsonify({}), 200

@app.route('/addFriend', methods=['POST'])
def addFriend():
    return jsonify({}), 200

@app.route('/deleteFriend', methods=['DELETE'])
def deleteFriend():
    return jsonify({}), 200

@app.route('/addTask', methods=['POST'])
def addTask():
    return jsonify({}), 200

@app.route('/getAllTasks')
def getAllTasks():
    return jsonify({}), 200

@app.route('/updateTask', methods=['PUT'])
def updateTask():
    return jsonify({}), 200

@app.route('/deleteTask', methods=['DELETE'])
def deleteTask():
    return jsonify({}), 200

if __name__ == '__main__':
    app.run()