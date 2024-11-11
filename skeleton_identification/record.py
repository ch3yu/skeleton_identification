import cv2
import argparse
import pykinect_azure as pykinect

if __name__ == "__main__":
	# Parse command line argument
	parser = argparse.ArgumentParser()
	parser.add_argument("path_to_vid", help="Path to directory that stores the video")
	args = parser.parse_args()

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries()

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED

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
			break