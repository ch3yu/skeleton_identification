import cv2
import argparse
import pykinect_azure as pykinect
import json

if __name__ == "__main__":
	# Parse command line argument
	parser = argparse.ArgumentParser()
	parser.add_argument("path_to_vid", help="Path to directory that stores the video")
	args = parser.parse_args()

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries()
	
    # Modify camera configuration
	with open(r".\\device_config.json", 'r') as file:
		device_config_param = json.load(file)
		
	device_config = eval(device_config_param["default_configuration"])
	device_config.color_format = eval(device_config_param["color_format"])
	device_config.color_resolution = eval(device_config_param["color_resolution"])
	device_config.depth_mode = eval(device_config_param["depth_mode"])


	# Start device
	video_filename = args.path_to_vid
	device = pykinect.start_device(config=device_config, record=True, record_filepath=video_filename)

	cv2.namedWindow('Color image',cv2.WINDOW_NORMAL)
	while True:

		# Get capture
		capture = device.update()

		# Get the color depth image from the capture
		ret, color_image = capture.get_color_image()

		if not ret:
			continue
			
		# Plot the image
		cv2.imshow('Color image',color_image)
		
		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):
			print("The recording is terminated by user.")
			break