#Here's an example Python script that reads CSV data from KrakenSDR and sends it to the Jetson device over HTTP:

import time
import csv

while True:

    # Set the IP address and port of the computer to send the data to
    ip_address = '192.168.1.100' # <--- Enter desired computer IP here
    port = 5000 # TCP Port 5000

    # Read the CSV data from KrakenSDR
    with open('mydata.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for column in list(reader):
            longitude = column['I'] #Latitude Column
            latitude = column['J'] #Longitude Column
            confidence = column['C'] #Confidence Column
    
    # Send the CSV data to the Jetson device using HTTP POST request
    #url = 'http://0.0.0.0:8080/DOA_value.html' 
    #response = requests.post(url, json=data)

    # Print the HTTP response status code
    #print(f"HTTP response status code: {response.status_code}")

    message = f"{'I'},{'J'},{'C'}"
    
    # Wait for some time before sending the next request
    time.sleep(1)