from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # receiver_node = Node(
    #     package = 'nodecomx',
    #     executable = 'receiver'
    # )

    processing_node = Node(
        package = 'nodecomx',
        executable = 'processing'
    )

    # transmitter_node = Node(
    #     package = 'nodecomx',
    #     executable = 'transmitter'
    # )

    # ld.add_action(receiver_node)
    ld.add_action(processing_node)
    # ld.add_action(transmitter_node)

    return ld
