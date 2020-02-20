import requests

url = 'http://localhost:5000/'
r = requests.post(url,json={'experience':'https://saleor.io/'})

print(r.json())
