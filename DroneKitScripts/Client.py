import requests
import json

class Client():

	def send_get(endpoint):
		response = requests.get(endpoint)
		print(response.status_code)

		if response.status_code == 200: #can also be written as if response:
			print('Success!')
		elif response.status_code == 404:
			print('Error: Not Found')

		response.encoding = 'utf-8'
		print(response.text)

	# gets data as dictionary
	def send_post(endpoint, data):
		# convert to json
		post = json.dumps(data)
		# send data 
		requests.post(endpoint, post)
	
