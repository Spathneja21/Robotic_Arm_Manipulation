import os

from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # The URDF is authored in ur3_gripper_description, not here - this is
    # the one place that has to know its path. `sim_ignition: false,
    # use_fake_hardware: true` is what makes this runnable with no Gazebo
    # at all: see ur3_ros2_control.xacro's mock_components/GenericSystem
    # branch, added specifically for this launch file.
    xacro_path = os.path.join(
        get_package_share_directory("ur3_gripper_description"),
        "urdf",
        "ur3_with_gripper.urdf.xacro",
    )

    moveit_config = (
        MoveItConfigsBuilder("ur3_gripper", package_name="ur3_moveit_config")
        .robot_description(
            file_path=xacro_path,
            mappings={"sim_ignition": "false", "use_fake_hardware": "true"},
        )
        .robot_description_semantic()
        .robot_description_kinematics()
        .joint_limits()
        .trajectory_execution()
        .planning_pipelines()
        .planning_scene_monitor()
        .to_moveit_configs()
    )

    return generate_demo_launch(moveit_config)
