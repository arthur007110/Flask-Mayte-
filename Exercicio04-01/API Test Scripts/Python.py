import requests

url = "http://localhost:5000/register"

headers = {
    'cache-control': "no-cache",
    'postman-token': "e983879b-28e6-9fb0-a822-71d4aa058f16"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)