import csv
import time

with open('Krakenoutput.csv', 'r') as csvfile:
    # Create a CSV reader object
    reader = csv.reader(csvfile)    # Reads csv file from krakensdr
    with open('KrakenOutputSim.csv', 'w', encoding = 'UTF8', newline = '') as f: 
        writer = csv.writer(f)
        for row in reader: 
            print('writing')
            writer.writerow(row)
            time.sleep(1)
