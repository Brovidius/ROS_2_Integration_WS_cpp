import rclpy
from sensor_salinity import salinity_data_publisher_node as node


def main(args=None):
    rclpy.init(args=args)
    
    # Construct the publisher
    salinity_data_publisher = node.SalinityDataPublisher()

    # Reading and publishing data at defined rate (2 seconds)
    rclpy.spin(salinity_data_publisher)

    # Clean up when script is stopped
    salinity_data_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()