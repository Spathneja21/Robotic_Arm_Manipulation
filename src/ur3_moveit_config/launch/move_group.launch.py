import os

from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
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
    return generate_move_group_launch(moveit_config)
