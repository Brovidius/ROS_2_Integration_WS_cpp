cmake_minimum_required(VERSION 3.8)
project(evocomx)

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

include_directories(include)

# Create publisher executable
add_executable(publisher src/publisher.cpp)
ament_target_dependencies(publisher rclcpp std_msgs)

# Create PubSub executable
add_executable(comEvo src/working.cpp)
ament_target_dependencies(comEvo rclcpp std_msgs)

# Create PubSub executable
add_executable(comEvo2 src/working2.cpp)
ament_target_dependencies(comEvo2 rclcpp std_msgs)

# Install Cpp executables
install(TARGETS
  publisher
  comEvo
  comEvo2
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
