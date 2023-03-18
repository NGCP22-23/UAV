import csv
import requests

# Define the URL of the remote server
#url = 'http://remote.server.com/data/upload'

# Open the CSV file
with open('Krakenoutput.csv', 'r') as csvfile:
    # Create a CSV reader object
    reader = csv.reader(csvfile)

    final_line = csvfile.readlines()[-1]
    longitude = final_line[1]
    print(longitude)
    # # Loop through the rows in the CSV file
    # for column in reader:
    #     # Extract the longitude, latitude, and confidence values from the row
    #     longitude = column[0]
    #     latitude = column[1]
    #     confidence = column[2]

    #     # Create a dictionary of the data to send
    #     data = {
    #         'longitude': longitude,
    #         'latitude': latitude,
    #         'confidence': confidence
    #     }
        
        # Send the data to the remote server using HTTP POST request
        #response = requests.post(url, data=data)

        # Print the response from the remote server
        # if(confidence >= 90):
        #     print(data.longitude)
        #     print(data.latitude)
        #     print(data.confidence)
        # if(confidence < 90):
        #     print(data.longitude)
        #     print(data.latitude)
        #     print(data.confidence)
        #     print("Warning: Confidence values are lower than expected")