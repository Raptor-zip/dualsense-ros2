from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('publish_rate', default_value='100.0'),
        DeclareLaunchArgument('player', default_value='1'),
        DeclareLaunchArgument('l2_threshold', default_value='20'),
        DeclareLaunchArgument('r2_threshold', default_value='20'),
        DeclareLaunchArgument('stick_deadzone', default_value='8'),

        Node(
            package='dualsense',
            executable='dualsense_node',
            name='dualsense_node',
            output='screen',
            parameters=[{
                'publish_rate': LaunchConfiguration('publish_rate'),
                'player': LaunchConfiguration('player'),
                'l2_threshold': LaunchConfiguration('l2_threshold'),
                'r2_threshold': LaunchConfiguration('r2_threshold'),
                'stick_deadzone': LaunchConfiguration('stick_deadzone'),
            }],
        ),
    ])
