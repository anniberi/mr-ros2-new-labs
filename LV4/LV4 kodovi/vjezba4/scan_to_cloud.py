#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, PointCloud2
import laser_geometry.laser_geometry as lg


class ScanToCloud(Node):
    def __init__(self):
        super().__init__('scan_to_cloud')
        self.lp = lg.LaserProjection()
        self.sub = self.create_subscription(LaserScan, '/scan', self.callback, 10)
        self.pub = self.create_publisher(PointCloud2, '/scan_cloud', 10)
        self.get_logger().info('Scan-to-Cloud converter running...')

    def callback(self, msg):
        try:
            cloud = self.lp.projectLaser(msg)
            self.pub.publish(cloud)
        except Exception as e:
            self.get_logger().warn(f"Conversion failed: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = ScanToCloud()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
