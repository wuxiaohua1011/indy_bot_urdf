import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os


def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(
        package="roar-gokart-urdf"
    ).find("roar-gokart-urdf")
    default_model_path = os.path.join(pkg_share, "src/gokart/main.urdf")

    robot_state_publisher_node = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {"robot_description": Command(["xacro ", LaunchConfiguration("model")])}
        ],
    )
    joint_state_publisher_node = launch_ros.actions.Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        condition=launch.conditions.UnlessCondition(
            LaunchConfiguration("gui", default="False")
        ),
    )

    return launch.LaunchDescription(
        [
            launch.actions.DeclareLaunchArgument(
                name="model",
                default_value=default_model_path,
                description="Absolute path to robot urdf file",
            ),
            joint_state_publisher_node,
            robot_state_publisher_node,
        ]
    )
