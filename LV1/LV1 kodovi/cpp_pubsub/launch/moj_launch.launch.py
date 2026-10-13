import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable


def generate_launch_description():
    # === Launch arguments ===
    model_arg = DeclareLaunchArgument(
        'model',
        default_value='waffle',
        description='TurtleBot3 model type [burger, waffle, waffle_pi]'
    )

    # === Set environment variable for the model ===
    set_model_env = SetEnvironmentVariable(
        name='TURTLEBOT3_MODEL',
        value=LaunchConfiguration('model')
    )

    # === Get package paths ===
    tb3_gazebo_dir = get_package_share_directory('turtlebot3_gazebo')
    tb3_bringup_dir = get_package_share_directory('turtlebot3_bringup')

    # === Include Gazebo launch ===
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_gazebo_dir, 'launch', 'empty_world.launch.py')
        )
    )

    # === Include RViz launch ===
    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_bringup_dir, 'launch', 'rviz2.launch.py')
        )
    )

    # === Combine everything ===
    return LaunchDescription([
        model_arg,
        set_model_env,
        gazebo_launch,
        rviz_launch
    ])

