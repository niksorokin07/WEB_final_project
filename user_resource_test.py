from requests import get, post, delete, put
import datetime

print(get('http://127.0.0.1:8080/api/v2/users').json())
print(post('http://127.0.0.1:8080/api/v2/users', json={'email': 'test1@mars.org',
                                                       'surname': 'komarov', 'name': 'ivan', 'age': 22,
                                                       'position': '2', 'speciality': 'microbiologist',
                                                       'address': 'Novatorov 22A',
                                                       'password_hash': 'password',
                                                       'modified_date': None}).json())
print(put('http://127.0.0.1:8080/api/v2/users/7', json={'email': 'test2@mars.org',
                                                        'surname': 'komarov', 'name': 'ivan', 'age': 22,
                                                        'position': '2', 'speciality': 'microbiologist',
                                                        'address': 'Novatorov 22A',
                                                        'password_hash': 'password',
                                                        'modified_date': None}).json())
print(delete('http://127.0.0.1:8080/api/v2/users/4').json())
