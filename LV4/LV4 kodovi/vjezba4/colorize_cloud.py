#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs_py.point_cloud2 as pc2
from std_msgs.msg import Header
import numpy as np
import matplotlib.cm as cm

class ColorizeCloud(Node):
    def __init__(self):
        super().__init__('colorize_cloud')
        self.sub = self.create_subscription(PointCloud2, '/octomap_point_cloud_centers', self.callback, 10)
        self.pub = self.create_publisher(PointCloud2, '/colored_cloud', 10)
        self.get_logger().info('🎨 Colorizing /octomap_point_cloud_centers → /colored_cloud')

    def callback(self, msg):
        # Safely read XYZ points
        points_data = list(pc2.read_points(msg, field_names=('x', 'y', 'z'), skip_nans=True))
        if not points_data:
            self.get_logger().info('Waiting for OctoMap points...')
            return

        points = np.array(points_data)
        if points.dtype.names is not None:
            # Structured dtype (x, y, z fields)
            x, y, z = points['x'], points['y'], points['z']
            points = np.column_stack((x, y, z)).astype(np.float32)
        else:
            points = points.reshape(-1, 3).astype(np.float32)

        # Normalize Z for rainbow coloring
        z_vals = points[:, 2]
        z_min, z_max = z_vals.min(), z_vals.max()
        norm = (z_vals - z_min) / (z_max - z_min + 1e-9)

        # Convert normalized Z to RGB rainbow
        colors = (cm.jet(norm)[:, :3] * 255).astype(np.uint8)

        # Pack RGB bytes into a single float32 (as RViz expects)
        rgb_packed = (colors[:, 0].astype(np.uint32) << 16) | \
                     (colors[:, 1].astype(np.uint32) << 8) | \
                     (colors[:, 2].astype(np.uint32))
        rgb_packed = rgb_packed.view(np.float32)

        # Combine XYZ + packed RGB
        cloud_out = np.column_stack((points, rgb_packed))

        # Create output PointCloud2
        header = Header()
        header.stamp = msg.header.stamp
        header.frame_id = msg.header.frame_id

        fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
            PointField(name='rgb', offset=12, datatype=PointField.FLOAT32, count=1)
        ]

        cloud_msg = pc2.create_cloud(header, fields, cloud_out)
        self.pub.publish(cloud_msg)
        self.get_logger().info('✅ Published /colored_cloud with rainbow colors')

def main(args=None):
    rclpy.init(args=args)
    node = ColorizeCloud()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

