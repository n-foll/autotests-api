import httpx

login_payload = {
    "email": "user@example.com",
     "password": "string"
}

login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

print("Login response:", login_response_data)
print("Status Code:", login_response.status_code)

access_token = login_response_data["token"]["accessToken"]
headers = {
    "Authorization": f"Bearer {access_token}"
}


authorization_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=headers)
authorization_response_data = authorization_response.json()

print("User data response:", authorization_response_data)
print("Status Code:", authorization_response.status_code)
