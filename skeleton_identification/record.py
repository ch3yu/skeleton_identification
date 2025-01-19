import cv2
import argparse
import pykinect_azure as pykinect
import json

if __name__ == "__main__":
	# Parse command line argument
	parser = argparse.ArgumentParser()
	parser.add_argument("path_to_vid", help="Path to directory that stores the video")
	args = parser.parse_args()

	path_to_vid = args.path_to_vid

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries(track_body=True)
	
    # Modify camera configuration
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

	cv2.namedWindow('Color image',cv2.WINDOW_NORMAL)
	while True:
		capture = device.update()

		# body_frame = bodyTracker.update(capture=capture)

		# ret_color, color_image = capture.get_transformed_color_image()
		ret_color, color_image = capture.get_color_image()

		if not ret_color:
			continue

		# color_image = body_frame.draw_bodies(color_image)
			
		# Plot the image
		cv2.imshow('Color image', color_image)
		
		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):
			print("The recording is terminated by user.")
			break