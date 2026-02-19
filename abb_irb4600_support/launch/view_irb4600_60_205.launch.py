#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution,  LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

_PACKAGE_NAME = 'abb_irb4600_support'
_XACRO_FILE = 'preview_irb4600_60_205.urdf.xacro'
_TF_PREFIX_ARG = 'tf_prefix'

def generate_launch_description():
    abb_irb4600_support_share = FindPackageShare(_PACKAGE_NAME)

    tf_prefix_arg = DeclareLaunchArgument(
        _TF_PREFIX_ARG, 
        default_value='abb-', 
        description='Robot frame prefix'
    )
    tf_prefix = LaunchConfiguration(_TF_PREFIX_ARG)
    log_prefix = LogInfo(msg=['TF Prefix is: ', tf_prefix])

    description_file = PathJoinSubstitution([
        abb_irb4600_support_share, 
        'urdf', 
        'previews', 
        _XACRO_FILE
    ])

    robot_description_content = Command([
        FindExecutable(name='xacro'),
        ' ',
        description_file,
        ' ',
        'tf_prefix:=', tf_prefix,
    ])
    robot_description = {'robot_description': ParameterValue(value=robot_description_content, value_type=str)}

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[robot_description],
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
    )

    rviz_config_file = PathJoinSubstitution([abb_irb4600_support_share, 'rviz', 'view_abb_irb4600_60_205.rviz'])
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        arguments=['-d', rviz_config_file],
    )

    static_tf_world_to_base = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'world', [tf_prefix, 'base_link']],
        output='log',
    )

    return LaunchDescription([
        tf_prefix_arg,
        robot_state_publisher_node,
        joint_state_publisher_node,
        static_tf_world_to_base,
        rviz_node,
        log_prefix,
    ])
