from requests import get, exceptions, post, delete, put

"""try:
    print(get('http://localhost:8080/api/jobs').json())
except exceptions.ConnectionError:
    print("Connection 1 refused")
try:
    print(get('http://localhost:8080/api/jobs/1').json())
except exceptions.ConnectionError:
    print("Connection 2 refused")
try:
    print(get('http://localhost:8080/api/jobs/999').json())
except exceptions.ConnectionError:
    print("Connection 3 refused")
try:
    print(get('http://localhost:8080/api/jobs/s').json())
except exceptions.ConnectionError:
    print("Connection 4 refused")"""
"""
try:
    # Bad request
    print(post('http://localhost:8080/api/jobs').json())
    # Id already exist
    print(post('http://localhost:8080/api/jobs',
               json={"id": 1, "team_leader": "test-run@mars.org", "job": "test-run",
                     "work_size": 16, "hazard_level": 2, "collaborators": None, "start_date": None, "end_date": None,
                     "is_finished": False}).json())
    # Success
    print(post('http://localhost:8080/api/jobs',
               json={"id": 2, "team_leader": "test-run@mars.org", "job": "test-run",
                     "work_size": 16, "hazard_level": 2, "collaborators": None, "start_date": None, "end_date": None,
                     "is_finished": False}).json())
except exceptions.ConnectionError:
    print("Connections 5-8 refused")"""
"""
try:
    # Bad request
    print(delete('http://127.0.0.1:8080/api/jobs/99').json())
    # Success
    print(delete('http://127.0.0.1:8080/api/jobs/3').json())
    # Bad request (Id no longer exists)
    print(delete('http://127.0.0.1:8080/api/jobs/3').json())
except exceptions.ConnectionError:
    print("Connections 9-11 refused")"""
"""
try:
    # Bad request
    print(put('http://localhost:8080/api/jobs/1',
              json={"team_leader": "test-run@mars.org"}).json())
    # Id doesn't exist
    print(put('http://localhost:8080/api/jobs/99',
              json={"team_leader": "test-run@mars.org", "job": "test-run",
                    "work_size": 16, "hazard_level": 2, "collaborators": None, "start_date": None, "end_date": None,
                    "is_finished": False}).json())
    # Success
    print(put('http://localhost:8080/api/jobs/6',
              json={"team_leader": "test-run@mars.org", "job": "test-run",
                    "work_size": 16, "hazard_level": 2, "collaborators": None, "start_date": None, "end_date": None,
                    "is_finished": False}).json())
except exceptions.ConnectionError:
    print("Connections 12-14 refused")"""
