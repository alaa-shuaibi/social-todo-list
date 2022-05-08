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
def createUser(username, password, data):
    pass

# Login in to given user's account:
def login(username, password):
    pass

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