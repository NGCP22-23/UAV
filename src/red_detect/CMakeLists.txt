cmake_minimum_required(VERSION 3.5)
project(red_detect)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

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
find_package( OpenCV REQUIRED )

include_directories( &{OpenCV_INCLUDE_DIRS}
                      ${CMAKE_SOURCE_DIR}/include/red_detect
                    )

include_directories(include)

add_executable( ArrayPublisherExample src/arrayPublisher_example.cpp)
add_executable( ArraySubscriberExample src/arraySubscriber_example.cpp)
add_executable ( cudaCV src/cuda_cv.cpp)

add_library( NodeTools include/red_detect/NodeTools.cpp)
add_library( Diagnostics include/red_detect/Diagnostics.cpp)

#target_link_libraries( RedDetect ${OpenCV_LIBS} )

ament_target_dependencies( ArrayPublisherExample rclcpp std_msgs )
ament_target_dependencies( ArraySubscriberExample rclcpp std_msgs )
ament_target_dependencies( cudaCV rclcpp  std_msgs OpenCV )

ament_target_dependencies( NodeTools rclcpp std_msgs )
ament_target_dependencies( Diagnostics rclcpp std_msgs )

install(TARGETS
  ArrayPublisherExample
  ArraySubscriberExample
  NodeTools
  Diagnostics
  cudaCV
  DESTINATION lib/${PROJECT_NAME}
  )

ament_package()
