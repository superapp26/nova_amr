from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    pkg_share = FindPackageShare('nova_description')

    model = LaunchConfiguration('model')

    rviz_config = LaunchConfiguration('rviz_config')

    gui = LaunchConfiguration('gui')

    rviz = LaunchConfiguration('rviz')

    robot_description = ParameterValue(Command(['xacro ', model]), value_type=str)


    return LaunchDescription([

        DeclareLaunchArgument(
            'model',
            default_value=PathJoinSubstitution([pkg_share, 'urdf', 'nova.urdf.xacro']),
            description='Path to the robot xacro file'),
        DeclareLaunchArgument(
            'rviz_config',
            default_value=PathJoinSubstitution([pkg_share, 'rviz', 'view_robot.rviz']),
            description='Path to the RViz config file'),
        DeclareLaunchArgument(
            'gui', default_value='true',
            description='true: joint sliders window, false: joints stay at zero'),
        DeclareLaunchArgument(
            'rviz', default_value='true',
            description='Start RViz'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
            ),
        # Publishes /joint_states for the wheel joints

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            condition=IfCondition(gui),
            ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            condition=UnlessCondition(gui),
            ),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            condition=IfCondition(rviz),
            ),
    ])
