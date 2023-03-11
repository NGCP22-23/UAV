#Here's an example Python script that reads CSV data from KrakenSDR and sends it to the Jetson device over HTTP:

import requests
import time
import csv

while True:
    # Read the CSV data from KrakenSDR
    with open('kraken_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    # Send the CSV data to the Jetson device using HTTP POST request
    url = 'http://jetson_ip_address/csv_data_receiver'
    response = requests.post(url, json=data)

    # Print the HTTP response status code
    print(f"HTTP response status code: {response.status_code}")

    # Wait for some time before sending the next request
    time.sleep(1)
