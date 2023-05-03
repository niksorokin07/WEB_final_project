from requests import get, post, put, delete

print(get('http://127.0.0.1:8080/api/v2/products').json())
print(
    post('http://127.0.0.1:8080/api/v2/products',
         json={'name': "testing", "price": 650, "description": "This is a test subject", "image": "avatar.jpg",
               "owner": 1, 'categories': "1, 2"}).json())
print(
    put('http://127.0.0.1:8080/api/v2/products/23',
        json={'name': "testing", "price": 650, "description": "This is a test subject", "image": "avatar.jpg",
              "owner": 1, 'categories': "1, 2"}).json())
print(delete('http://127.0.0.1:8080/api/v2/products/23').json())
