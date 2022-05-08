import pymongo
from pymongo.errors import ConnectionFailure
import bcrypt

# Connect to MongoDB database:
host = 'localhost:27017'
client = pymongo.MongoClient('mongodb://' + host)

try:
    client.admin.command('ping')
except ConnectionFailure:
    print("Server not available")
    exit()

db = client['social_todo_list']

# Creates a new user account:
def createUser(username, password):
    user_creds_coll = db['user_creds']
    user_data_coll = db['user_data']

    salt = bcrypt.gensalt()

    user_creds = {
        '_id': username,
        'salt': salt,
        'password': bcrypt.hashpw(password.encode('utf-8'), salt)
    }

    user_data = {
        '_id': username,
        'first_name': '',
        'last_name': '',
        'description': '',
        'status': '',
        'friend_list': [],
        'todo_list': [
            {
                'task': 'Finish setting up account.',
                'type': 'basic',
                'isPublic': False,
            },
            {
                'task': 'Finish tutorial.',
                'type': 'course',
                'isPublic': False
            }
        ]
    }

    user_creds_coll.insert_one(user_creds)
    user_data_coll.insert_one(user_data)

    return db['user_data'].find_one({'_id': username})

# Login in to given user's account and return user's data:
def login(username, password):
    try:
        salt = db['user_creds'].find_one({'_id': username}, {'_id': False, 'salt': True})['salt']
    except:
        return {'error': 'Could not find user.'}
    
    result = db['user_creds'].find_one({'_id': username, 'password': bcrypt.hashpw(password.encode('utf-8'), salt)})

    try:
        if result['_id'] != username:
            return {'error': 'Incorrect password.'}
    except:
        return {'error': 'Incorrect password.'}

    return db['user_data'].find_one({'_id': username})

# Update the given user's data (data only contains updated data):
def updateUserData(username, data):
    pass

# Delete the given user's account:
def deleteUser(username, password):
    pass

# Add a friend to the friend list:
def addFriend(username, friend_username):
    pass

# Remove a friend from the friend list:
def removeFriend(friend_username):
    pass

# Add a task to the to-do list:
def addTask(username, data):
    pass

# Get all the tasks of a given user:
def getAllTasks(username):
    pass

# Update the given task:
def updateTask(task):
    pass

# Delete the given task:
def deleteTask(username, task):
    pass