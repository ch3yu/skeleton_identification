import cv2
import argparse
import pykinect_azure as pykinect
import json
import helper as helper
import numpy as np
import ctypes

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="<record> for record mode, <offline> for offline mode")
    parser.add_argument("path_to_vid", help="Path to the video")
    args = parser.parse_args()

    mode = args.mode
    path_to_vid = args.path_to_vid

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (0, 0, 255)
    thickness = 2

    if mode != "record" and mode != "offline":
        print("The program does not support {mode} mode.\nPlease input either <record> or <offline>.".format(mode=mode))

    # Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries(track_body=True)

    if mode == "record":
        with open(r".\\device_config.json", 'r') as file:
            device_config_param = json.load(file)
            
        device_config = eval(device_config_param["default_configuration"])
        device_config.color_format = eval(device_config_param["color_format"])
        device_config.color_resolution = eval(device_config_param["color_resolution"])
        device_config.depth_mode = eval(device_config_param["depth_mode"])
        device = pykinect.start_device(config=device_config, record=True, record_filepath=path_to_vid)
        
        tracker_config = pykinect.default_tracker_configuration
        tracker_config.sensor_orientation = pykinect.K4ABT_SENSOR_ORIENTATION_DEFAULT
        tracker_config.tracker_processing_mode = pykinect.K4ABT_TRACKER_PROCESSING_MODE_GPU
        tracker_config.gpu_device_id = 0
        bodyTracker = pykinect.start_body_tracker()
        
    elif mode == "offline":
        device = pykinect.start_playback(path_to_vid)
        device_config = device.get_record_configuration()
        device_calibration = device.get_calibration()
        tracker_config = pykinect.default_tracker_configuration
        tracker_config.tracker_processing_mode =pykinect.K4ABT_TRACKER_PROCESSING_MODE_GPU
        bodyTracker = pykinect.start_body_tracker(calibration=device_calibration, tracker_configuration=tracker_config)

    cv2.namedWindow("Color image with skeleton", cv2.WINDOW_NORMAL)

    frame = 0
    while True:
        if mode == "record":
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
                print("The recording is terminated by user.")
                break

        elif mode == "offline":
            ret, capture = device.update()

            if not ret:
                break

            body_frame = bodyTracker.update(capture=capture)
            
            color_image_object = capture.get_color_image_object()
            color_format = color_image_object.get_format()
            if color_format != pykinect.k4a._k4atypes.K4A_IMAGE_FORMAT_COLOR_BGRA32:
                _, m = color_image_object.to_numpy()
                bgra = cv2.cvtColor(m, cv2.COLOR_BGR2BGRA)
                bgra_image_handle = pykinect.k4a._k4a.k4a_image_t()
                image_format = pykinect.k4a._k4a.K4A_IMAGE_FORMAT_COLOR_BGRA32
                buffer = bgra.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
                pykinect.k4a._k4a.VERIFY(pykinect.k4a._k4a.k4a_image_create_from_buffer(image_format, bgra.shape[1], bgra.shape[0], bgra.shape[1]*4, buffer, bgra.nbytes, ctypes.c_void_p(0), ctypes.c_void_p(0), bgra_image_handle), "MJPG to BGRA32 ERROR")
                color_image_object = pykinect.k4a.Image(bgra_image_handle)

                ret_color, color_image = capture.camera_transform.color_image_to_depth_camera(capture.get_depth_image_object(), color_image_object).to_numpy()
            else:
                ret_color, color_image = capture.get_transformed_color_image()

            timestamp = pykinect.k4a._k4a.k4a_image_get_timestamp_usec(capture.get_color_image_object().handle())

            if not ret_color:
                continue

            color_image = body_frame.draw_bodies(color_image)

            id_features = np.load(f"id_features_{path_to_vid[0:-4]}.npy")

            num_bodies = body_frame.get_num_bodies()
            for body_idx in range(num_bodies):
                skeleton = body_frame.get_body_skeleton(body_idx)
                features = helper.calculate_features(skeleton)
                
                body_id = helper.find_closest_match(features, id_features[:, :, frame], threshold=0.05)
                body_2d = body_frame.get_body2d(body_idx)
                
                timestamp_coord = [10, 20]
                text_coord = body_2d.joints[pykinect.k4abt._k4abtTypes.K4ABT_JOINT_NECK].get_coordinates()
                color_image = cv2.putText(color_image, str(body_id), text_coord, font, fontScale, color, thickness, cv2.LINE_AA)
                color_image = cv2.putText(color_image, str(timestamp), timestamp_coord, font, fontScale, color, thickness, cv2.LINE_AA)

                cv2.imshow('Color image with skeleton', color_image)
            frame = frame + 1

            if cv2.waitKey(1) == ord('q'):
                print("The recording is terminated by user.")
                break