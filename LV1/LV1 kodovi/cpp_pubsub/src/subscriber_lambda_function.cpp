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
#include "geometry_msgs/msg/twist.hpp"

class SubscribeThenPublish : public rclcpp::Node
{
public:
  SubscribeThenPublish()
  : Node("subscribe_then_publish")
  {
    
    // Publisher for modified message:
    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("novi_topic", 10);
    
    auto topic_callback =
      [this](const geometry_msgs::msg::Twist::UniquePtr msg) -> void {
        RCLCPP_INFO(this->get_logger(), "I heard: linear.x=%.2f, linear.y=%.2f, linear.z=%.2f, angular.x=%.2f, angular.y=%.2f, angular.z=%.2f", msg->linear.x, msg->linear.y, msg->linear.z, msg->angular.x, msg->angular.y, msg->angular.z);
        
        auto nova_msg = geometry_msgs::msg::Twist();
      
        nova_msg.linear.x = msg->linear.x * 2.0;
        nova_msg.linear.y = msg->linear.y * 2.0;
        nova_msg.linear.z = msg->linear.z * 2.0;

        nova_msg.angular.x = -msg->angular.x;
        nova_msg.angular.y = -msg->angular.y;
        nova_msg.angular.z = -msg->angular.z;
        
        RCLCPP_INFO(this->get_logger(),
            "Publishing: linear.x=%.2f linear.y=%.2f linear.z=%.2f angular.x=%.2f angular.y=%.2f angular.z=%.2f", nova_msg.linear.x, nova_msg.linear.y, nova_msg.linear.z, nova_msg.angular.x, nova_msg.angular.y, nova_msg.angular.z);
            
        publisher_->publish(nova_msg);
      };
    subscription_ =
      this->create_subscription<geometry_msgs::msg::Twist>("topic", 10, topic_callback);
      
      
      
  }

private:
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
  rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SubscribeThenPublish>());
  rclcpp::shutdown();
  return 0;
}
