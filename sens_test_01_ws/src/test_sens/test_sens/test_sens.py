# Import required modules
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class  Test_sens(Node):

    def __init__(self):

        # Call the constructor of the parent class
        super().__init__('test_node_sens')

        # Type of message for publish/subscribe for ROS 2
        self.msg = String()

        # This timer is necessarry in order to initiate this cycle, which will in turn initiate 
        # the other nodes as well-
        self.timer = self.create_timer(1, self.publish_callback)

        # ROS 2 publisher
        self.publisher_ = self.create_publisher(String, 'oxygen_data', 1)
        # Call the function

        self.mindummevariabel = 1

    def publish_callback(self):
        self.msg.data = "42.24242"
        self.publisher_.publish(self.msg)

def main():
    
    # Basic ROS2 stuff. Recommending to just read the documentation for these.

    rclpy.init(args=None)
    rclpy.spin(Test_sens()) # Runs the node in a loop
    
    # Once loop ends, things get deleted
    Test_sens.destroy_node() 
    rclpy.shutdown()

if __name__ == "__main__":
    main()



