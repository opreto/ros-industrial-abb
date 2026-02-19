cmake_minimum_required(VERSION 3.8)
project(abb_irb4600_support)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch urdf meshes config
  DESTINATION share/${PROJECT_NAME}/
  USE_SOURCE_PERMISSIONS
)

install(DIRECTORY rviz
  DESTINATION share/${PROJECT_NAME}/
  OPTIONAL
)

ament_package()
