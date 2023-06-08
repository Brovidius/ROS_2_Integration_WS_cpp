
# Import required modules
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


# Import of homemade modules
import nodecomx.algo as my_algo
import nodecomx.FP16_converter as FP16_converter
# This module contains our modem information which is used among all local nodes.
from nodecomx.modem_info import *

# Define ProcessingNode class, which inherits from the Node class
class ProcessingNode(Node):

    def __init__(self):

        # Call the constructor of the parent class
        super().__init__(f'processing_node_{modem_name}')

        # Type of message for publish/subscribe for ROS 2
        self.msg = String()
        # self.ROV_data
        # self.ox_data

        # ROS 2 publisher and subscriber       
        self.publisher_transmitter = self.create_publisher(String, f'/topic_transmission{modem_name}', 1)
        self.publisher_ROV = self.create_publisher(String, '/odom2', 1)

        self.subscription_reception = self.create_subscription(String, f'/topic_reception{modem_name}', self.reception_callback, 1)
        # self.subscription_sensor = self.create_subscription(String, 'oxygen_data', self.sensor_callback, 1)
        self.subscription_ROV = self.create_subscription(String, '/bluerov2_pid/bluerov2/observer/nlo/odom_ned', self.ROV_callback, 1)
        # self.subscription # To ignore unimportant errors. Recommended by ROS 2 documentation.

    def reception_callback(self, msg):

        received_message = msg.data
        if isinstance(received_message[0], str):
            newData = [int(i) for i in received_message]
        else:
            newData = received_message

        incoming_message_to_unsigned = [it + 256 if it <= -1 else it for it in newData]   
        incoming_message = FP16_converter.Converter.int8_list_to_FP16(incoming_message_to_unsigned)
        msg.data = str(incoming_message)
        self.publisher_ROV.publish(msg)
        
    def ROV_callback(self, msg):
        converted_ROV_data = FP16_converter.Converter.FP16_list_to_int8(msg.data)
        msg.data = str(converted_ROV_data)
        self.publisher_transmitter.publish(msg)

def main():

    # Basic ROS2 stuff. Recommending to just read the documentation for these.
    rclpy.init(args=None)
    rclpy.spin(ProcessingNode()) # Runs the node in a loop
    # Once loop ends, things get deleted
    ProcessingNode.destroy_node() 
    rclpy.shutdown()

if __name__ == "__main__":
    main()
