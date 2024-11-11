import cv2
import argparse
import pykinect_azure as pykinect

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="<record> for record mode, <offline> for offline mode")
    parser.add_argument("path_to_vid", help="Path to the video")
    args = parser.parse_args()

    mode = args.mode
    path_to_vid = args.path_to_vid

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (0, 0, 255)
    thickness = 2

    if mode != "record" and mode != "offline":
        print("The program does not support {mode} mode.\nPlease input either <record> or <offline>.".format(mode=mode))

    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries(track_body=True)

    if mode == "record":
        device_config = pykinect.default_configuration
        device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
        device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
        device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
        device = pykinect.start_device(config=device_config, record=True, record_filepath=path_to_vid)
        
        tracker_config = pykinect.k4abt._k4abtTypes.k4abt_tracker_default_configuration
        tracker_config.sensor_orientation = pykinect.K4ABT_SENSOR_ORIENTATION_DEFAULT
        tracker_config.tracker_processing_mode = pykinect.K4ABT_TRACKER_PROCESSING_MODE_GPU
        tracker_config.gpu_device_id = 0
        bodyTracker = pykinect.start_body_tracker()

    elif mode == "offline":
        device = pykinect.start_playback(path_to_vid)
        device_config = device.get_record_configuration()
        device_calibration = device.get_calibration()
        bodyTracker = pykinect.start_body_tracker(calibration=device_calibration)

    cv2.namedWindow("Color image with skeleton", cv2.WINDOW_NORMAL)

    while True:
        capture = device.update()

        body_frame = bodyTracker.update(capture=capture)

        ret_color, color_image = capture.get_transformed_color_image()

        if not ret_color:
            continue

        color_image = body_frame.draw_bodies(color_image)

        num_bodies = body_frame.get_num_bodies()
        for body_idx in range(num_bodies):
            body_id = body_frame.get_body_id(body_idx)
            body_2d = body_frame.get_body2d(body_idx)
            text_coord = body_2d.joints[pykinect.k4abt._k4abtTypes.K4ABT_JOINT_NECK].get_coordinates()
            color_image = cv2.putText(color_image, str(body_id), text_coord, font, fontScale, color, thickness, cv2.LINE_AA)

            cv2.imshow('Color image with skeleton', color_image)

        if cv2.waitKey(1) == ord('q'):
            break