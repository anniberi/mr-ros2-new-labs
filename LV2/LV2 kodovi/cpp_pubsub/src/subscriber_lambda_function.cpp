// Copyright 2016 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
//#include "geometry_msgs/msg/twist.hpp"
#include "geometry_msgs/msg/twist_stamped.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2/LinearMath/Matrix3x3.h"
#include "cmath"

const double x_cilj = 3.0;
const double y_cilj = 3.0;

class SubscribeThenPublish : public rclcpp::Node {
public:
  SubscribeThenPublish() : Node("subscribe_then_publish") {
    
    // Publisher for modified message:
    publisher_ = this->create_publisher<geometry_msgs::msg::TwistStamped>("/cmd_vel", 10);
    subscription_ = this->create_subscription<nav_msgs::msg::Odometry>("/odom", 10, std::bind(&SubscribeThenPublish::odom_callback, this, std::placeholders::_1));
      
  }

private:  
  void odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg) {
    double x_robot = msg->pose.pose.position.x;
    double y_robot = msg->pose.pose.position.y;
    
    tf2::Quaternion q(
      msg->pose.pose.orientation.x,
      msg->pose.pose.orientation.y,
      msg->pose.pose.orientation.z,
      msg->pose.pose.orientation.w
    );
    
    double roll, pitch, yaw;
    tf2::Matrix3x3(q).getRPY(roll, pitch, yaw);
    
    double dx = x_cilj - x_robot;
    double dy = y_cilj - y_robot;
    double distance = std::sqrt(dx*dx + dy*dy);
    double target_angle = std::atan2(dy, dx);
    double angle_diff = target_angle - yaw;
    
    // Normalizacija ugla:
    while(angle_diff > M_PI) angle_diff -= 2*M_PI;
    while(angle_diff < -M_PI) angle_diff += 2*M_PI;
    
    /*geometry_msgs::msg::Twist cmd_vel;
    
    if(distance > 0.1) {
      cmd_vel.linear.x = 0.2 * distance;
      cmd_vel.angular.z = 0.5 * angle_diff;
    } else {
      cmd_vel.linear.x = 0;
      cmd_vel.angular.z = 0;
    }*/
    
    geometry_msgs::msg::TwistStamped cmd_vel;
  cmd_vel.header.stamp = this->now();
  cmd_vel.header.frame_id = "base_link";
  cmd_vel.twist.linear.x = 0.2 * distance;
  cmd_vel.twist.angular.z = 0.5 * angle_diff;

    
    
    publisher_->publish(cmd_vel);
    
    RCLCPP_INFO(this->get_logger(), "Pozicija robota: (%.2f, %.2f), ugao = %.2f, cilj = (%.2f, %.2f), udaljenost = %.2f, razlika_uglova = %.2f", x_robot, y_robot, yaw, x_cilj, y_cilj, distance, angle_diff);
  }
  rclcpp::Publisher<geometry_msgs::msg::TwistStamped>::SharedPtr publisher_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr subscription_;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SubscribeThenPublish>());
  rclcpp::shutdown();
  return 0;
}
