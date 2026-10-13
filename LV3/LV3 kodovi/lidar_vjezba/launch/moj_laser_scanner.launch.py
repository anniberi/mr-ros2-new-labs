from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='odom_to_moj_base_tf',
            arguments=['1.0', '0', '0', '0', '0', '0', 'odom', 'moj_base_link']
        ),
        
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='moj_base_to_laser_tf',
            arguments=['0', '0', '0.2', '0', '0', '0', 'moj_base_link', 'moj_laser']
        ),


        Node(
            package='lidar_vjezba',
            executable='moj_scan_pubsub',
            name='moj_scan_pubsub_node',
            output='screen'
        )
    ])
