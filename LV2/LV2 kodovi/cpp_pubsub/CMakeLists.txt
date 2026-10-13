cmake_minimum_required(VERSION 3.8)
project(cpp_pubsub)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2 REQUIRED)

add_executable(talker src/publisher_lambda_function.cpp)
target_link_libraries(talker PUBLIC rclcpp::rclcpp ${geometry_msgs_TARGETS})

add_executable(listener src/subscriber_lambda_function.cpp)
target_link_libraries(listener PUBLIC rclcpp::rclcpp tf2::tf2 ${nav_msgs_TARGETS} ${std_msgs_TARGETS} ${geometry_msgs_TARGETS})

install(TARGETS
  talker
  listener
  DESTINATION lib/${PROJECT_NAME})
  
# Install launch files
install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)


ament_package()
