import httpx

from tools.fakers import fake

# Создаем пользователя
create_user_payload = {
    "email": fake.email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}
create_user_response = httpx.post("http://localhost:8000/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()
print('Create user data:', create_user_response_data)

# Проходим аутентификацию
login_payload = {
    "email": create_user_payload['email'],
    "password": create_user_payload['password']
}

login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print('Login data:', login_response_data)

update_payload = {
    "email": fake.email(),
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

headers = {
    "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
}
user_id = create_user_response_data["user"]["id"]

update_response = httpx.patch(
    f"http://localhost:8000/api/v1/users/{user_id}",
    json=update_payload,
    headers=headers
)

update_response_data = update_response.json()

print('Update response status:', update_response.status_code)
print('Update response data:', update_response_data)