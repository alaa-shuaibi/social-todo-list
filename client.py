# File used to test requests to the server.
import json, requests, sys, getpass

host = sys.argv[1]
username = sys.argv[2]

# All available requests to make:
get_requests = ['getAllTasks']
post_requests = ['addFriend', 'addTask']
put_requests = ['updateProfile', 'updateTask']
delete_requests = ['deleteProfile', 'deleteFriend', 'deleteTask']

# Authentication:
response = requests.get(host + 'login', json={
    'username': username,
    'password': getpass.getpass('Enter password: ')
})

print('\nStatus Code: ' + str(response.status_code))

if response.status_code == 401:
    print('Incorrect password.')
    exit()
elif response.status_code == 404:
    print('Creating new account...')
    try:
        response = requests.post(host + 'signup', json={
            'username': username,
            'password': getpass.getpass('Enter password: ')
        })
    except:
        print('Failed to create a new account.')
        exit()
    print('Successfully created a new account!')
elif response.ok == False:
    print('Failed to login in.')
    exit()
else:
    print('Successfully logged in!')
    print('User Info:\n' + response.content.decode())

while True:
    path = input('Enter a request (e.g., "getAllTasks"): ')
    url = host + path
    filename = input('Enter name of file containing data: ')
    print('')

    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            data['username'] = username
    except:
        data = {
            'username': username
        }

    if (path in get_requests):
        response = requests.get(url, json=data)
    elif (path in post_requests):
        response = requests.post(url, json=data)
    elif (path in put_requests):
        response = requests.put(url, json=data)
    elif (path in delete_requests):
        response = requests.delete(url, json=data)
    else:
        print('Not a valid request. Please try again.\n')
        continue
    
    print('Status Code: ' + str(response.status_code))
    print('Content:\n' + response.content.decode() + '\n')