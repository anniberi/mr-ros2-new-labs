from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', '/home/anniberi/berina_ws/src/vjezba4/rviz/rtabmap_view.rviz'],
            output='screen'
        )
    ])

