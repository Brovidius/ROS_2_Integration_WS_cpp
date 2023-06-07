# Import required modules
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from unetpy import *

# This module contains our modem information which is used among all local nodes.
from nodecomx.modem_info import *

class TransmitterNode(Node):

    def __init__(self):

        # Call the constructor of the parent class
        super().__init__(f'transmitter_node_{modem_name}')
        
        # For UnetStack reception. See official documentation for correct settings.
        self.sock = UnetSocket(modem_ip, portnumber)
        self.phy = self.sock.agentForService(Services.PHYSICAL)
                         
        # Type of message for publish/subscribe for ROS 2
        self.msg = String()
        # ROS 2 subscriber
        self.subscription = self.create_subscription(String, f'topic_transmission{modem_name}', self.subscribe_callback, 1)
        self.subscription  # To ignore unimportant errors. Recommended by ROS 2 documentation.
    
    def subscribe_callback(self, msg):
        # Cleaning up the msg.data so we transmitt a list of integers instead of a string of a list
        stripped_array = msg.data.strip('][').split(', ')
        integer_array = [int(i) for i in stripped_array]

        # Broadcasting using the physical service of UnetStack API
        self.phy << TxJanusFrameReq(classUserID = 16, appData = 7, data = integer_array)

def main():

    # Basic ROS2 stuff. Recommending to just read the documentation for these.
    rclpy.init(args=None)
    rclpy.spin(TransmitterNode()) # Runs the node in a loop
    # Once loop ends, things get deleted
    TransmitterNode.destroy_node() 
    rclpy.shutdown()

if __name__ == "__main__":
    main()


