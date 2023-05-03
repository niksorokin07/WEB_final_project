from requests import get, post, delete, put

print(get('http://127.0.0.1:8080/api/v2/users').json())
print(post('http://127.0.0.1:8080/api/v2/users', json={'email': 'test3@icloud.org',
                                                       'surname': 'komarov', 'name': 'ivan',
                                                       'address': 'Novatorov 22A',
                                                       'password_hash': 'password',
                                                       'balance': 0}).json())
print(put('http://127.0.0.1:8080/api/v2/users/4', json={'email': 'test1@icloud.org',
                                                        'surname': 'komarov', 'name': 'ivan',
                                                        'address': 'Novatorov 22A',
                                                        'password_hash': 'password',
                                                        'balance': 0}).json())
print(delete('http://127.0.0.1:8080/api/v2/users/4').json())
