from requests import get, post, put, delete

print(get('http://127.0.0.1:8080/api/v2/jobs').json())
print(
    post('http://127.0.0.1:8080/api/v2/jobs', json={'team_leader': "nikso@mars.org", 'job': 'test-run', 'work_size': 1,
                                                    'collaborators': '1,2,3', 'hazard_level': 1,
                                                    'is_finished': False}).json())
print(
    put('http://127.0.0.1:8080/api/v2/jobs/7', json={'team_leader': "nikso@mars.org", 'job': 'test-run', 'work_size': 1,
                                                     'collaborators': '1,2,3', 'hazard_level': 1,
                                                     'is_finished': False}).json())
print(delete('http://127.0.0.1:8080/api/v2/jobs/7').json())
