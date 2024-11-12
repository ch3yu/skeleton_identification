# Skeleton Identification
## About
Skeleton identificatioin is a program used to map humans captured with Azure Kinect with their skeleton representations. It is achieved by overlaying RGB images with the 3D skeletons present in frames and write their skeleton IDs next to them.

There are important files in the **skeleton_identification** directory, including **main.py**, **record.py**, and **device_configuration.json**. **main.py** is designed to overlay 3D skeletons of humans over their RGB representaions and display the results on the screen. To execute the program, user has to input `python main.py <mode> <path_to_file>` in the command prompt. The program supports two modes: `record` and `offline`, which can be used to record a video or process a pre-recorded data, repsectively. As for `<path_to_file>` is used to assign the location to store the data or retrieve the pre-recorded video, depending on the `<mode>` chosen.

Another important file in the directory is **record.py**, which is intended to record new videos. Users can use this program by typing `python record.py <path_to_file>`, where `<path_to_file>` is the destination to store the recorded data. We purposefully design a module for this function to save computational power while recording. Even though **main.py** also supports recording, it is intended to demonstrate the overlapping of 3D skeletons and RGB images. **record.py** supports recording without laying 3D skeletons on RGB images, which is less computationally intensive.

As for **device_configuration.json**, it documents the parameters required to create videos that can generate 3D skeletons. Both **main.py** and **reocrd.py** retrieves the device configuration parameters from this file.

## Acknowledgement
This repository uses and adapts code from [pyKinectAzure](https://github.com/ibaiGorordo/pyKinectAzure/tree/master).
