import pykinect_azure as pykinect
import numpy as np
import json
import os

from pykinect_azure.k4abt import _k4abtTypes

def calculate_features(skeleton):
    joints = skeleton.joints

    head_to_spine_x = joints[_k4abtTypes.K4ABT_JOINT_HEAD].position.xyz.x - joints[_k4abtTypes.K4ABT_JOINT_PELVIS].position.xyz.x
    head_to_spine_y = joints[_k4abtTypes.K4ABT_JOINT_HEAD].position.xyz.y - joints[_k4abtTypes.K4ABT_JOINT_PELVIS].position.xyz.y
    head_to_spine_z = joints[_k4abtTypes.K4ABT_JOINT_HEAD].position.xyz.z - joints[_k4abtTypes.K4ABT_JOINT_PELVIS].position.xyz.z

    arm_length_x = joints[_k4abtTypes.K4ABT_JOINT_HANDTIP_RIGHT].position.xyz.x - joints[_k4abtTypes.K4ABT_JOINT_SHOULDER_RIGHT].position.xyz.x
    arm_length_y = joints[_k4abtTypes.K4ABT_JOINT_HANDTIP_RIGHT].position.xyz.y - joints[_k4abtTypes.K4ABT_JOINT_SHOULDER_RIGHT].position.xyz.y
    arm_length_z = joints[_k4abtTypes.K4ABT_JOINT_HANDTIP_RIGHT].position.xyz.z - joints[_k4abtTypes.K4ABT_JOINT_SHOULDER_RIGHT].position.xyz.z

    leg_length_x = joints[_k4abtTypes.K4ABT_JOINT_HIP_LEFT].position.xyz.x - joints[_k4abtTypes.K4ABT_JOINT_KNEE_LEFT].position.xyz.x
    leg_length_y = joints[_k4abtTypes.K4ABT_JOINT_HIP_LEFT].position.xyz.y - joints[_k4abtTypes.K4ABT_JOINT_KNEE_LEFT].position.xyz.y
    leg_length_z = joints[_k4abtTypes.K4ABT_JOINT_HIP_LEFT].position.xyz.z - joints[_k4abtTypes.K4ABT_JOINT_KNEE_LEFT].position.xyz.z

    head_to_spine = np.linalg.norm([head_to_spine_x, head_to_spine_y, head_to_spine_z])
    arm_length = np.linalg.norm([arm_length_x, arm_length_y, arm_length_z])
    leg_length = np.linalg.norm([leg_length_x, leg_length_y, leg_length_z])

    return [head_to_spine, arm_length, leg_length]


def find_closest_match(features, stored_features, threshold=0.05):
    closest_id = None
    min_distance = float("inf")

    for person_id in range(stored_features.shape[0]):
        stored_feats = stored_features[person_id, :]
        distance = np.linalg.norm(np.array(features) - stored_feats)

        if distance < threshold and distance < min_distance:
            closest_id = person_id
            min_distance = distance        

    return closest_id + 1


if __name__ == "__main__":
    pass