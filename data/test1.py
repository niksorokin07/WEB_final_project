from requests import get , exceptions , post , delete , put

'''
try:
    print(get('http://localhost:8080/api/users').json())
except exceptions.ConnectionError:
    print("Connection 1 refused")
try:
    print(get('http://localhost:8080/api/users/2').json())
except exceptions.ConnectionError:
    print("Connection 2 refused")
try:
    print(get('http://localhost:8080/api/users/999').json())
except exceptions.ConnectionError:
    print("Connection 3 refused")
try:
    print(get('http://localhost:8080/api/users/s').json())
except exceptions.JSONDecodeError:
    print("Wrong type of parameter, expected int")
'''
'''
try:
    # Bad request
    print(post('http://localhost:8080/api/users').json())
    # Id already exist
    print(post('http://localhost:8080/api/users',
               json={'id': 1, 'email': 'test3@icloud.org',
                     'surname': 'komarov', 'name': 'ivan',
                     'address': 'Novatorov 22A',
                     'password_hash': 'password',
                     'balance': 0}).json())
    # Success
    print(post('http://localhost:8080/api/users',
               json={'id': 4, 'email': 'tes5@icloud.org',
                     'surname': 'komarov', 'name': 'ivan',
                     'address': 'Novatorov 22A',
                     'password_hash': 'password',
                     'balance': 0}).json()
except exceptions.ConnectionError:
    print("Connections 5-8 refused")'''
'''
try:
    # Bad request
    print(delete('http://127.0.0.1:8080/api/users/99').json())
    # Success
    print(delete('http://127.0.0.1:8080/api/users/1').json())
    # Bad request (Id no longer exists)
    print(delete('http://127.0.0.1:8080/api/users/7').json())
except exceptions.ConnectionError:
    print("Connections 9-11 refused")
'''
'''
try:
    # Bad request
    print(put('http://localhost:8080/api/users/1' ,
              json={"owner": "test-run@mars.org"}).json())
    # Id doesn't exist
    print(put('http://localhost:8080/api/users/99' ,
              json={'email': 'test3@icloud.org' ,
                    'surname': 'komarov' , 'name': 'ivan' ,
                    'address': 'Novatorov 22A' ,
                    'password_hash': 'password' ,
                    'balance': 0}).json())
    # Success
    print(put('http://localhost:8080/api/users/6' ,
              json={'email': 'test1@icloud.org' ,
                    'surname': 'komarov' , 'name': 'ivan' ,
                    'address': 'Novatorov 22A' ,
                    'password_hash': 'password' ,
                    'balance': 0}).json())
except exceptions.ConnectionError:
    print("Connections 12-14 refused")
'''
