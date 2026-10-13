from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode
from lifecycle_msgs.msg import Transition
from launch_ros.events.lifecycle import ChangeState


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # --- Define the SLAM Toolbox lifecycle node ---
    slam_toolbox_node = LifecycleNode(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        namespace='',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'odom_frame': 'odom',
            'base_frame': 'base_footprint',
            'scan_topic': '/scan',
            'slam_params_file': '/opt/ros/kilted/share/slam_toolbox/config/mapper_params_online_async.yaml'
        }],
    )

    # --- Emit lifecycle events manually ---
    configure = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=lambda n: n == slam_toolbox_node,
            transition_id=Transition.TRANSITION_CONFIGURE,
        )
    )
    activate = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=lambda n: n == slam_toolbox_node,
            transition_id=Transition.TRANSITION_ACTIVATE,
        )
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        slam_toolbox_node,
        configure,
        activate,
    ])

