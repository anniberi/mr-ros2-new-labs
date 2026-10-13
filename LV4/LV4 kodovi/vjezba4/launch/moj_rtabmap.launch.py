from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # --- Bridge camera topics from Gazebo to ROS 2 ---
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='rgb_camera_bridge',
            arguments=['/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image'],
            output='screen'
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='depth_camera_bridge',
            arguments=['/camera/depth/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked'],
            output='screen'
        ),

        # --- Optional bridge for laser scan ---
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='scan_bridge',
            arguments=['/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan'],
            output='screen'
        ),

        # --- TF and clock bridges ---
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='tf_bridge',
            arguments=['/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V'],
            output='screen'
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='clock_bridge',
            arguments=['/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock'],
            output='screen'
        ),

        # --- RTAB-Map SLAM node ---
        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'frame_id': 'base_link',
                'odom_frame_id': 'odom',
                'map_frame_id': 'map',
                'subscribe_depth': True,
                'subscribe_rgb': True,
                'subscribe_scan': True,             # Enable LIDAR
                'approx_sync': True,
                'rgb_topic': '/camera/image_raw',
                'depth_topic': '/camera/depth/points',
                'scan_topic': '/scan',
                'queue_size': 10,
                'publish_tf': True,
                'Grid/FromDepth': True,
                'Grid/DepthRays': 1,
                'Grid/MaxGroundHeight': 0.1,
                'Grid/RangeMax': 6.0,
                'Grid/CellSize': 0.05,              # smaller cells = higher map resolution
                'Grid/Sensor': 1,                   # 1=Depth camera, 2=Lidar, 3=both
                'Grid/NormalsK': 20,
                'Grid/ClusterRadius': 0.1,
                'Grid/MinClusterSize': 3,
                'Rtabmap/DetectionRate': 1.0,
                'Mem/IncrementalMemory': True,
                'RGBD/OptimizeFromGraphEnd': False,
                'RGBD/NeighborLinkRefining': True
            }],
            remappings=[
                ('rgb/image', '/camera/image_raw'),
                ('depth/image', '/camera/depth/points'),
                ('scan', '/scan')
            ],
        ),

        # --- RTAB-Map Visualization (RViz window + GUI) ---
        Node(
            package='rtabmap_viz',
            executable='rtabmap_viz',
            name='rtabmap_viz',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'frame_id': 'base_link'
            }],
            remappings=[
                ('rgb/image', '/camera/image_raw'),
                ('depth/image', '/camera/depth/points'),
                ('scan', '/scan')
            ]
        ),

        # --- Keyboard teleop ---
        Node(
            package='turtlebot3_teleop',
            executable='teleop_keyboard',
            name='teleop_keyboard',
            output='screen',
            prefix=['xterm -e']
        )
    ])

