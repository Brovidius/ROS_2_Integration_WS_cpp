from rclpy.node import Node

# tsys01 needed in order to utilize the BlueRobotics TSYS01 Python Library which must be installed
from sensor_salinity import catlas01
from sensor_interfaces.msg import Salinity
import time

class SalinityDataPublisher(Node):
    # Initializer 
    def __init__(self):
        super().__init__('SalinityDataPublisher')
        self.publisher_ = self.create_publisher(Salinity, 'salinity_data', 10)  # Creates a publisher over the topic salinity_data
        self.sample_time  = self.declare_parameter('sample_time', 2.0).value  # Gets sample time as a parameter, default = 2
        self.timer = self.create_timer(self.sample_time, self.salinity_read_and_publish)

        self.sensor = catlas01.CATLAS01()
        if not self.sensor.init():
            # If sensor can not be detected
            self.get_logger().error("Sensor could not be initialized (No bus)")
            exit(1)

    def salinity_read_and_publish(self):
        # Custom conductivity message to publish. Can be found in the brov2_interfaces.
        msg = Salinity()

        # Getting the local time 
        current_time = time.localtime()
        msg.local_time =  time.strftime("%H:%M:%S",current_time)

        # Reading salinity and loading data into custom message
        if self.sensor.read():
                msg.salinity_value     = self.sensor._salinity
        else:
                self.get_logger().error("Sensor read failed!")
                exit(1)

        # Publishing message and logging data sent over the topic /salinity_data
        self.publisher_.publish(msg)
        self.get_logger().info('\ttime: %s  S: %0.2f µs/cm' % (msg.local_time,
                                                               msg.salinity_value))
