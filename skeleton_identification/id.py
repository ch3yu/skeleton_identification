import json
import argparse
import pykinect_azure as pykinect
import helper
import numpy as np

if __name__ == "__main__":
    pykinect.initialize_libraries(track_body=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("num_subjects", help="<num_subjects> determines the number of subjects recorded")
    parser.add_argument("path_to_vid", help="Path to the video")
    args = parser.parse_args()

    num_features = 3
    num_subjects = int(args.num_subjects)
    path_to_vid = args.path_to_vid

    try:
        with open(f"id_features_{path_to_vid[0:-4]}.npy", "r") as features_file:
            print(f"id_features_{path_to_vid[0:-4]}.npy already exists.")
    except FileNotFoundError:
        device = pykinect.start_playback(path_to_vid)
        device_config = device.get_record_configuration()
        device_calibration = device.get_calibration()
        tracker_config = pykinect.default_tracker_configuration
        tracker_config.tracker_processing_mode =pykinect.K4ABT_TRACKER_PROCESSING_MODE_GPU
        bodyTracker = pykinect.start_body_tracker(calibration=device_calibration, tracker_configuration=tracker_config)

        id_features = np.zeros((num_subjects, num_features, 1))

        frame = 0
        while True:
            ret, capture = device.update()
            if not ret:
                np.save(f"id_features_{path_to_vid[0:-4]}.npy", id_features)
                break

            body_frame = bodyTracker.update(capture=capture)

            num_bodies = body_frame.get_num_bodies()                
            for body_idx in range(num_bodies):
                body_id = body_frame.get_body_id(body_idx)
                skeleton = body_frame.get_body_skeleton(body_idx)
                features = helper.calculate_features(skeleton)
                id_features[body_id-1, :, frame] = np.array(features)
            
            id_features = np.dstack((id_features, np.zeros((num_subjects, num_features))))
            frame = frame + 1