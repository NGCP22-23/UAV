import csv
import time

rowNumber = 0
with open('Krakenoutput.csv', 'r') as csvfile:
    # Create a CSV reader object
    reader = csv.reader(csvfile)    # Reads csv file from krakensdr
    with open('KrakenOutputSim.csv', 'w', encoding = 'UTF8', newline = '') as f: 
        writer = csv.writer(f)
        for row in reader: 
            print('writing')
            writer.writerow(row)
            print(rowNumber)
            rowNumber = rowNumber + 1
            time.sleep(1/4)
