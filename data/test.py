from requests import get, exceptions, post, delete, put

'''
try:
    print(get('http://localhost:8080/api/products').json())
except exceptions.ConnectionError:
    print("Connection 1 refused")
try:
    print(get('http://localhost:8080/api/products/2').json())
except exceptions.ConnectionError:
    print("Connection 2 refused")
try:
    print(get('http://localhost:8080/api/products/999').json())
except exceptions.ConnectionError:
    print("Connection 3 refused")
try:
    print(get('http://localhost:8080/api/products/s').json())
except exceptions.JSONDecodeError:
    print("Wrong type of parameter, expected int")'''
'''
try:
    # Bad request
    print(post('http://localhost:8080/api/products').json())
    # Id already exist
    print(post('http://localhost:8080/api/products',
               json={'id': 2, 'name': "testing", "price": 650, "description": "This is a test subject",
                     "image": "avatar.jpg",
                     "owner": 1, 'categories': "1, 2"}).json())
    # Success
    print(post('http://localhost:8080/api/products',
               json={'id': 1, 'name': "testing", "price": 650, "description": "This is a test subject",
                     "image": "avatar.jpg",
                     "owner": 1, 'categories': "1, 2"}).json())
except exceptions.ConnectionError:
    print("Connections 5-8 refused")'''
'''
try:
    # Bad request
    print(delete('http://127.0.0.1:8080/api/products/99').json())
    # Success
    print(delete('http://127.0.0.1:8080/api/products/1').json())
    # Bad request (Id no longer exists)
    print(delete('http://127.0.0.1:8080/api/products/1').json())
except exceptions.ConnectionError:
    print("Connections 9-11 refused")'''
'''
try:
    # Bad request
    print(put('http://localhost:8080/api/products/1',
              json={"owner": "test-run@mars.org"}).json())
    # Id doesn't exist
    print(put('http://localhost:8080/api/products/99',
              json={'name': "testing", "price": 650, "description": "This is a test subject",
                    "image": "avatar.jpg",
                    "owner": 1, 'categories': "1, 2"}).json())
    # Success
    print(put('http://localhost:8080/api/products/6',
              json={'id': 1, 'name': "testing", "price": 650, "description": "This is a test subject",
                    "image": "avatar.jpg",
                    "owner": 1, 'categories': "1, 2"}).json())
except exceptions.ConnectionError:
    print("Connections 12-14 refused")
'''
