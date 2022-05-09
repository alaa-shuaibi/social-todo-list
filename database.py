import pymongo
from pymongo.errors import ConnectionFailure
import bson
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

acceptable_profile_fields = ['new_username', 'first_name', 'last_name', 'description', 'status']
acceptable_task_fields = ['task', 'type', 'isPublic', 'start_date', 'duration', 'repeated_date', 'location', 'isRemote', 'users_shared_with']

# Creates a new user account:
def createUser(username, password):
    user_creds_coll = db['user_creds']
    user_data_coll = db['user_data']

    _id = bson.ObjectId()
    salt = bcrypt.gensalt()

    user_creds = {
        '_id': _id,
        'salt': salt,
        'password': bcrypt.hashpw(password.encode('utf-8'), salt)
    }

    user_data = {
        '_id': _id,
        'username': username,
        'first_name': '',
        'last_name': '',
        'description': '',
        'status': '',
        'friend_list': [],
        'todo_list': [
            {
                'task_id': str(bson.ObjectId()),
                'task': 'Finish setting up account.',
                'type': 'basic',
                'isPublic': False,
            },
            {
                'task_id': str(bson.ObjectId()),
                'task': 'Finish tutorial.',
                'type': 'course',
                'isPublic': False
            }
        ]
    }

    user_creds_coll.insert_one(user_creds)
    user_data_coll.insert_one(user_data)

    return db['user_data'].find_one({'username': username}, {'_id': False})

# Login in to given user's account and return user's data:
def login(username, password):
    try:
        oid = db['user_data'].find_one({'username': username})['_id']
        salt = db['user_creds'].find_one({'_id': oid}, {'_id': False, 'salt': True})['salt']
    except:
        return {'error': 'Could not find user.'}
    
    result = db['user_creds'].find_one({'_id': oid, 'password': bcrypt.hashpw(password.encode('utf-8'), salt)})
    
    try:
        if result['_id'] != oid:
            return {'error': 'Incorrect password.'}
    except:
        return {'error': 'Incorrect password.'}

    return db['user_data'].find_one({'username': username}, {'_id': False})

# Update the given user's data (data only contains updated data):
def updateUserData(username, data):
    curr_username = username

    for key in data:
        try:
            # Check if key is an acceptable field for user profile data:
            if key not in acceptable_profile_fields:
                continue

            # Update current username to new one:
            if key == 'new_username' & data['new_username'] != '':
                result = db['user_data'].update_one({'username': curr_username}, {'$set': {'username': data[key]}})
                if result.modified_count >= 1:
                    curr_username = data['new_username']
                continue

            result = db['user_data'].update_one({'username': curr_username}, {'$set': {key: data[key]}})
        except:
            continue
    
    return db['user_data'].find_one({'username': curr_username}, {'_id': False})

# Delete the given user's account:
def deleteUser(username, password):
    try:
        oid = db['user_data'].find_one({'username': username})['_id']
        salt = db['user_creds'].find_one({'_id': oid}, {'_id': False, 'salt': True})['salt']
    except:
        return {'error': 'Could not find user.'}
    
    try:
        result = db['user_creds'].delete_one({'_id': oid, 'password': bcrypt.hashpw(password.encode('utf-8'), salt)})
        if result.deleted_count >= 1:
            db['user_data'].delete_one({'_id': oid})
        else:
            return {'error': 'Failed to delete account.'}
    except:
        return {'error': 'Failed to delete account.'}

    return {'result': 'Successfully deleted account!'}

# Add a friend to the friend list:
def addFriend(username, friend_username):
    result = db['user_data'].update_one({'username': username}, {
        '$addToSet': {
            'friend_list': friend_username
        }
    })
    
    return db['user_data'].find_one({'username': username}, {'_id': False, 'friend_list': True})

# Remove a friend from the friend list:
def removeFriend(username, friend_username):
    result = db['user_data'].update_one({'username': username}, {
        '$pull': {
            'friend_list': friend_username
        }
    })

    return db['user_data'].find_one({'username': username}, {'_id': False, 'friend_list': True})

# Add a task to the to-do list:
def addTask(username, data):
    task_id = str(bson.ObjectId())
    result = db['user_data'].update_one({'username': username}, {
        '$addToSet': {
            'todo_list': {
                'task_id': task_id,
                'task': data['task'],
                'type': data['type'],
                'isPublic': data['isPublic']
            }
        }
    })

    for key in data:
        try:
            if key not in acceptable_task_fields or key in ['task_id', 'task', 'type', 'isPublic']:
                continue

            result = db['user_data'].update_one({'username': username, 'todo_list.task_id': task_id}, {
                '$set': {'todo_list.$.' + key: data[key]}
            })
        except:
            continue
    
    return db['user_data'].find_one({'username': username}, {'_id': False, 'todo_list': True})

# Get all the tasks of a given user:
def getAllTasks(username):
    try:
        return db['user_data'].find_one({'username': username}, {'_id': False, 'todo_list': True})
    except:
        return {'error': 'Could not retrieve tasks.'}

# Update the given task:
def updateTask(username, data):
    task_id = data['task_id']

    for key in data:
        try:
            if key not in acceptable_task_fields:
                continue

            result = db['user_data'].update_one({'username': username, 'todo_list.task_id': task_id}, {
                '$set': {'todo_list.$.' + key: data[key]}
            })
        except:
            continue
    
    return db['user_data'].find_one({'username': username}, {'_id': False, 'todo_list': True})

# Delete the given task:
def deleteTask(username, task_id):
    result = db['user_data'].update_one({'username': username}, {
        '$pull': {
            'todo_list': {'task_id': task_id}
        }
    })

    return db['user_data'].find_one({'username': username}, {'_id': False, 'todo_list': True})