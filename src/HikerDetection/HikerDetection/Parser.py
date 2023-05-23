import csv
import time

import rclpy 
from rclpy.node import Node
from std_msgs.msg import String

# Define the URL of the remote server
#url = 'http://remote.server.com/data/upload'

# Update 1.0:
# We want to read the KrakenSim starting with the last row. Then a counter should increment so it outputs each following row.

# Update 1.1: 
# The Parser is reading data from the KrakenOutputSim.csv, however the data is being updated 4 lines at a time. As a result, the Parser is 
# only outputting every 4 lines. 

# Update 1.2: A counter (nextRow) is added to replace the [-1] last line idea. The issue now is to fine a way to start the counter from the last line

# Update 1.3: Added another csv.reader to count the number of rows in the file. This needed for the file to start at the same line of the 
# KrakenSim.py output and to build off on it when counting future data. 

# Update 1.4: A sleep(1/2) is required before the start of the while loop to prevent the loop from starting before the next KrakenSim cycle.
class HikerDetection(Node):
    
    def __init__(self):
        super().__init__('kraken_node')

        # ros publisher topics
        self.kraken_publisher = self.create_publisher(String, 'kraken', 10)
        self.ready_publisher = self.create_publisher(bool, 'is_found', 10)
        # # set rate of publishing 
        # self.timer_period = 1   #1 second(1Hz)
        # self.timer = self.create_timer(self.timer_period, self.mode_callback(self.latest_message))

        self.latest_message,self.longitude,self.latitude,self.confidence,self.nextRow = 0,0,0,0,0

        #moving file opening into init

        ###this processes the csv data as a 
        #print("longitude ", ' | ' , "  latitude  ", ' | ', "confidence")
        with open('./HikerDetection/HikerDetection/KrakenOutputSim.csv', 'r') as csvfile:
            # Create a CSV reader object
            csv_reader = csv.reader(csvfile)
            
            # Get the total number of rows in the file
            num_rows = len(list(csv_reader))
            
            # Reset the file pointer to the beginning of the file
            csvfile.seek(0)
            
            # Create a new CSV reader object
            csv_reader = csv.reader(csvfile)
            
            # Get the row number of the last row
            for row_num, row in enumerate(csv_reader):
                if row_num == num_rows - 1:
                    nextRow = row_num
                    print(nextRow)
                    break


        time.sleep(1/2) # Necessary to prevent 
        while self.confidence < 8.3: 
            # Open the CSV file
            with open('./HikerDetection/HikerDetection/KrakenOutputSim.csv', 'r') as csvfile:
                time.sleep(1/2)
                final_line = csvfile.readlines()[nextRow]    # Pulls data from the last line of the csv file (most updated)
                lastRow = final_line.split(',') # Converts string of data into elements in a list seperated by a ,
                self.longitude = lastRow[8]  # Longitude coordinates
                self.latitude = lastRow[9]   # Latitude coordinates
                self.confidence = float(lastRow[3])   # Confidence values

                # self.latest_message = (longitude,
                #                        "latitude":latitude,
                #                        "confidence":confidence, 
                #                        "nextRow":nextRow}
                
                self.mode_callback()
                

    def mode_callback(self):
        # build the message
        msg = String()
        telem = (str(self.longitude),
                 str(self.latitude),
                 str(self.confidence),
                 str(self.nextRow),
                 )
        msg.data = '\n'.join(telem)
        
        # publish the data 
        self.kraken_publisher.publish(msg)
        
        # publish to console
        self.get_logger().info('Publishing: "%s"' % msg.data)

    def call(self):   
        confidence = -1
        nextRow = 0
        #print("longitude ", ' | ' , "  latitude  ", ' | ', "confidence")
        with open('KrakenOutputSim.csv', 'r') as csvfile:
            # Create a CSV reader object
            csv_reader = csv.reader(csvfile)
            
            # Get the total number of rows in the file
            num_rows = len(list(csv_reader))
            
            # Reset the file pointer to the beginning of the file
            csvfile.seek(0)
            
            # Create a new CSV reader object
            csv_reader = csv.reader(csvfile)
            
            # Get the row number of the last row
            for row_num, row in enumerate(csv_reader):
                if row_num == num_rows - 1:
                    nextRow = row_num
                    print(nextRow)
                    break

            #time.sleep(1)
            #final_line = csvfile.readlines()[num_rows]    # Pulls data from the last line of the csv file (most updated)
            #lastRow = final_line.split(',') # Converts string of data into elements in a list seperated by a ,
            #longitude = lastRow[8]  # Longitude coordinates
            #latitude = lastRow[9]   # Latitude coordinates
            #confidence = float(lastRow[3])   # Confidence values
            #print(longitude, ' | ' , latitude, ' | ', confidence)

        time.sleep(1/2) # Necessary to prevent 
        while confidence < 8.3: 
            # Open the CSV file
            with open('KrakenOutputSim.csv', 'r') as csvfile:
                time.sleep(1/2)
                final_line = csvfile.readlines()[nextRow]    # Pulls data from the last line of the csv file (most updated)
                lastRow = final_line.split(',') # Converts string of data into elements in a list seperated by a ,
                longitude = lastRow[8]  # Longitude coordinates
                latitude = lastRow[9]   # Latitude coordinates
                confidence = float(lastRow[3])   # Confidence values

                self.latest_message = {"longitude":longitude,
                                       "latitude":latitude,
                                       "confidence":confidence, 
                                       "nextRow":nextRow}

                nextRow = nextRow + 1
            
def main(args=None):
    rclpy.init(args=args)

    hiker = HikerDetection()

    # spin runs the callback functions
    rclpy.spin(hiker)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    HikerDetection.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()