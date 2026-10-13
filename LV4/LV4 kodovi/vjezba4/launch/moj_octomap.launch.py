from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1) Convert /scan (LaserScan) → /scan_cloud (PointCloud2)
        Node(
            package='vjezba4',
            executable='scan_to_cloud',
            name='scan_to_cloud',
            output='screen'
        ),

        # 2) Run Octomap server on /scan_cloud
        Node(
            package='octomap_server',
            executable='octomap_server_node',
            name='octomap_server',
            output='screen',
            parameters=[{
                'frame_id': 'odom',
                'resolution': 0.05,
                'sensor_model/max_range': 5.0,
            }],
            remappings=[
                ('cloud_in', '/scan_cloud'),
            ]
        ),

        # 3) Optional: colorized output (if you still want it)
        Node(
            package='vjezba4',
            executable='colorize_cloud',
            name='colorize_cloud',
            output='screen'
        ),
    ])

