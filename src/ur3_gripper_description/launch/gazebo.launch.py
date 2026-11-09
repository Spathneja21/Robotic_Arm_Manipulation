from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    xacro_path = PathJoinSubstitution(
        [FindPackageShare("ur3_gripper_description"), "urdf", "ur3_with_gripper.urdf.xacro"]
    )
    robot_description = {"robot_description": Command(["xacro ", xacro_path])}

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"])
        ),
        launch_arguments={"gz_args": "-r empty.sdf"}.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "robot_description", "-name", "ur3_gripper", "-z", "0.01"],
        output="screen",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )
    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller"],
    )
    gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper_controller"],
    )

    return LaunchDescription(
        [
            gz_sim,
            robot_state_publisher,
            spawn,
            # Controller spawners must wait for `spawn` to exit: that's the
            # moment the robot actually exists in the controller_manager.
            RegisterEventHandler(
                OnProcessExit(
                    target_action=spawn,
                    on_exit=[
                        joint_state_broadcaster_spawner,
                        arm_controller_spawner,
                        gripper_controller_spawner,
                    ],
                )
            ),
        ]
    )
