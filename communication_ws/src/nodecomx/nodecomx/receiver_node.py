# Import required modules
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from unetpy import *
from datetime import datetime

# This module contains our modem information which is used among all local nodes.
from nodecomx.modem_info import *


# int JANUS_RX_PORT = 9955;
# int JANUS_TX_PORT = 9955;
# string IP = "192.168.0.189";
# float STREAMFS = 250000.0;

# Define the function signature
#     Evo_janusXsdm::connection modem(IP, JANUSPATH, SDMPATH, JANUS_RX_PORT, JANUS_TX_PORT, STREAMFS); //Constructing a connection object;

class  ReceiverNode(Node):

    def __init__(self):

        # Call the constructor of the parent class
        super().__init__(f'receiver_node_{modem_name}')

        # Create a socket and agent for the Unet service
        self.sock = UnetSocket(modem_ip, portnumber)
        self.phy = self.sock.agentForService(Services.PHYSICAL)
        
        # For UnetStack reception. See official documentation for correct settings.
        self.phy << RxJanusFrameNtf(appData = 7, classUserID = 16)
        self.phy[3].frameLength = 40

        # Clearing the buffer
        self.phy.ClearReq
        
        # The initialization message. Only runs once at the start of the node.
        self.old_msg = [0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0,]
        
        # Type of message for publish/subscribe for ROS 2
        self.msg = String()

        # This timer is necessarry in order to initiate this cycle, which will in turn initiate 
        # the other nodes as well-
        self.timer = self.create_timer(1, self.publish_callback)

        # ROS 2 publisher
        self.publisher_ = self.create_publisher(String, f'topic_reception{modem_name}', 1)
        # Call the function

        self.mindummevariabel = 1

    def publish_callback(self):
        
        # UnetStack reception API. 
        rx = self.sock.getGateway().receive(RxJanusFrameNtf, timeout=5000)
        
        # If the message has been received
        if rx:
            print(rx.data)

            # The received data is likely a list that contains strings of something.
            # Depending on how the communication is processed, the data needs to be cleaned a bit.
            # If we are receiving a list of 8bit integers then we're fine.
            # However if we receive signed 8bit integers, then we need some conversion.

            # If the contents are in strings we wish to convert them to integers.
            if isinstance(rx.data[0], str):
                newData = [int(i) for i in rx.data]
            else:
                newData = rx.data

            # Now if the contents have signed integers, as in values from -128 to -1 then
            # we wish to change them into unsigned 8bit integers for our setup to work.
            # If there are none then it doesn't change the values.
            converted_list_to_unsigned = [it + 256 if it <= -1 else it for it in newData]

            # Now that the received data is cleaned, the entire list will be made into a string
            # for ROS2 publication.
            self.msg.data = str(converted_list_to_unsigned)

            # Since our reception was successfull, the default data should be change into the last 
            # received data. If communication breaks then the process can continue on old data.
            # If for some reason we do not wish to do that then commenting the line under should 
            # work, but mind that nothing will be published and the ROS2 stream will be on hold.
            # This means that processing_node.py will also be on hold, which means transmission_node.py
            # will also be on hold until a new publication is made from here. Unless processing_node
            # still has enough data to keep processing and publishing to transmission_node. 

            self.old_msg = self.msg.data           
            self.publisher_.publish(self.msg)
            print(f'Message {self.msg.data} published to topic.')
        

        # These next two ifs are for initialization of communication, since every node would
        # be waiting for a reception but no one would broadcast anything. Only do this once before
        # a no reception messages.

        if not rx and self.mindummevariabel == 1:
                
            print('No recepetion. ' + str(datetime.now().strftime("%H:%M:%S")))
            self.msg.data = str(self.old_msg) # First time message for initialization
            self.publisher_.publish(self.msg) # Publishing the message to topic_reception
            self.mindummevariabel = 0 # To lock this 'if' from running again

        if not rx:
                
            print('No recepetion. ' + str(datetime.now().strftime("%H:%M:%S")))
 

def main():
    
    # Basic ROS2 stuff. Recommending to just read the documentation for these.

    rclpy.init(args=None)
    rclpy.spin(ReceiverNode()) # Runs the node in a loop
    
    # Once loop ends, things get deleted
    ReceiverNode.destroy_node() 
    rclpy.shutdown()

if __name__ == "__main__":
    main()



