import requests

# Insert
requests.post("http://127.0.0.1:5000/insert", json={
    "id": 1,
    "name": "Amrutha"
})

# Get data
response = requests.get("http://127.0.0.1:5000/get/1")

print(response.json())