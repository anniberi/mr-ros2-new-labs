cmake_minimum_required(VERSION 3.8)
project(lidar_vjezba)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

add_executable(lidar_pubsub src/lidar_pubsub.cpp)
target_link_libraries(lidar_pubsub PUBLIC rclcpp::rclcpp ${geometry_msgs_TARGETS} ${sensor_msgs_TARGETS})

add_executable(moj_scan_pubsub src/moj_scan_pubsub.cpp)
target_link_libraries(moj_scan_pubsub PUBLIC rclcpp::rclcpp ${sensor_msgs_TARGETS})

install(TARGETS
 lidar_pubsub
 DESTINATION lib/${PROJECT_NAME})
 
install(TARGETS moj_scan_pubsub DESTINATION lib/${PROJECT_NAME})
 
 install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)



if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

