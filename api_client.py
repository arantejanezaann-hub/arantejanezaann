
import requests

name = input("Enter your first name: ")

url = "https://arantejanezaann-1.onrender.com/hello?name=Janeza"

params = {"name": name}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data["message"])
else:
    print("Request failed.")
    print("Status Code:", response.status_code)
