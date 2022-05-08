# File used to test requests to the server.
import json, requests, sys, getpass, pprint as pp

host = sys.argv[1]
username = sys.argv[2]

# All available requests to make:
get_requests = ['getAllTasks']
post_requests = ['addFriend', 'addTask']
put_requests = ['updateAccount', 'updateTask']
delete_requests = ['deleteAccount', 'deleteFriend', 'deleteTask']

# User authentication:
response = requests.post(host + 'login', json={
    'username': username,
    'password': getpass.getpass('Enter password: ')
})

print('\nStatus Code: ' + str(response.status_code))

if response.status_code == 401:
    print('Incorrect password.')
    exit()
elif response.status_code == 404:
    print('Create a new account:')
    try:
        response = requests.post(host + 'signup', json={
            'username': username,
            'password': getpass.getpass('Enter password: ')
        })
        print('\nStatus Code: ' + str(response.status_code))
        if response.ok == False:
            exit()
    except:
        print('Failed to create a new account.')
        pp.pprint(response.json())
        exit()
    print('Successfully created a new account!')
    print('User Data:\n')
    pp.pprint(response.json())
elif response.ok == False:
    print('Failed to login in.')
    exit()
else:
    print('Successfully logged in!')
    print('User Data:\n')
    pp.pprint(response.json())

while True:
    path = input('\nEnter a request (e.g., "getAllTasks"): ')
    url = host + path
    print('')

    try:
        with open('data.json', 'r') as f:
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
    print('Content:\n')
    pp.pprint(response.json())