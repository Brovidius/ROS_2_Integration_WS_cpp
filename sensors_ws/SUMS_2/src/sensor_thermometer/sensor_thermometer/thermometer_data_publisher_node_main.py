import rclpy
from sensor_thermometer import thermometer_data_publisher_node as node


def main(args=None):
    rclpy.init(args=args)
    
    # Construct the publisher
    thermometer_data_publisher = node.ThermometerDataPublisher()

    # Reading and publishing data at defined rate (2 seconds)
    rclpy.spin(thermometer_data_publisher)

    # Clean up when script is stopped
    thermometer_data_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()