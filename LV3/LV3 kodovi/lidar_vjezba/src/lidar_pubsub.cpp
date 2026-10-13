#include <memory>
#include <limits>
#include <cmath>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/point_stamped.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

using namespace std::chrono_literals;

class LidarPubSub : public rclcpp::Node {
public:
  LidarPubSub() : Node("lidar_pubsub") {
    publisher_ = this->create_publisher<geometry_msgs::msg::PointStamped>("/najbliza_tacka", 10);
    subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>("/scan", 10, std::bind(&LidarPubSub::scan_callback, this, std::placeholders::_1));
    
    RCLCPP_INFO(this->get_logger(), "LidarPubSub cvor pokrenut");
  }

private:
  void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg) {
    // Prvo stavimo minimalnu distancu na beskonacno:
    double min_dist = std::numeric_limits<double>::infinity();
    int min_index = -1;
    
    for(size_t i = 0; i < msg->ranges.size(); i++) {
      double r = msg->ranges[i];
      if(std::isfinite(r) && r < min_dist) min_dist = r, min_index = int(i);
    }
    
    if(min_index == -1) {
      RCLCPP_WARN(this->get_logger(), "Nema prepreka u blizini!");
      return;
    }
    
    // Treba ugao sad izracunati:
    double angle = msg->angle_min + min_index * msg->angle_increment;
    
    // Prebacivanje iz polarnih u normalne koordinate:
    geometry_msgs::msg::PointStamped point_msg;
    
    point_msg.header.stamp = this->now();
    point_msg.header.frame_id = "base_scan";
    
    point_msg.point.x = min_dist * std::cos(angle);
    point_msg.point.y = min_dist * std::sin(angle);
    point_msg.point.z = 0;
    
    // Publishanje:
    publisher_->publish(point_msg);
    
    RCLCPP_INFO(this->get_logger(), "Najbliza tacka: (x = %.2f, y = %.2f, r = %.2f, ugao = %.2f stepeni)", point_msg.point.x, point_msg.point.y, min_dist, angle * 180.0 / M_PI);
  }
  
  rclcpp::Publisher<geometry_msgs::msg::PointStamped>::SharedPtr publisher_;
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<LidarPubSub>());
  rclcpp::shutdown();
  return 0;
}
