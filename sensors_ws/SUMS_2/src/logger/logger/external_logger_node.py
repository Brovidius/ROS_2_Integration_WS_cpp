from rclpy.node import Node
from sensor_interfaces.msg import Modem
import datetime
import csv
import os

class ExternalLoggerNode(Node):

    def __init__(self):
        super().__init__('external_logger')

        self.header  = self.declare_parameter('log_header', '').value  # Gets header as a parameter

        # Fetches local date and time
        current_date = datetime.datetime.now().strftime("%d_%m_%Y")
        current_time = datetime.datetime.now().strftime("%H_%M_%S")

        # Builds file name and destination
        directory = 'log_data/'+ current_date + '/external/'
        self.file = directory + 'external_log_' + current_time + '.csv'

        # Creating a new directroy if none exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Opens a new .csv file
        with open(self.file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow([self.header])

        self.external_modem_subscription = self.create_subscription(
            Modem, 
            '/modem/external_data', 
            self.external_logger_callback, 
            10)

    def external_logger_callback(self, msg:Modem):
        data = msg.external_data
        with open(self.file, 'a', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow([data])