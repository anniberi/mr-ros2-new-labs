#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/laser_scan.hpp>

class MojScanPubSub : public rclcpp::Node {
public:
  MojScanPubSub() : Node("moj_scan_pubsub") {
    sub_ = create_subscription<sensor_msgs::msg::LaserScan>(
        "/scan", 10,
        [this](const sensor_msgs::msg::LaserScan::SharedPtr msg) {
          auto new_msg = *msg;
          new_msg.header.frame_id = "moj_laser";
          pub_->publish(new_msg);
        });

    pub_ = create_publisher<sensor_msgs::msg::LaserScan>("/moj_scan", 10);
    RCLCPP_INFO(get_logger(), "Node moj_scan_pubsub started!");
  }

private:
  rclcpp::Publisher<sensor_msgs::msg::LaserScan>::SharedPtr pub_;
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr sub_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MojScanPubSub>());
  rclcpp::shutdown();
  return 0;
}
