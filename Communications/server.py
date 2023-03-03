import requests

requests.get('http://127.0.0.1:5000/UAV')
response = requests.get('http://127.0.0.1:5000/UAV')

print(response.status_code)

if response.status_code == 200: #can also be written as if response:
	print('Success!')
elif response.status_code == 404:
	print('Error: Not Found')

response.encoding = 'utf-8'
response.content
print(response.text)
response.headers
