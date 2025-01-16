# Skeleton Identification
## About
Skeleton identificatioin is a program used to map humans captured with Azure Kinect with their skeleton representations. It is achieved by overlaying RGB images with the 3D skeletons present in frames and write their skeleton IDs next to them.

There are important files in the **skeleton_identification** directory, including **main.py**, **record.py**, **helper.py**, **id.py**, and **device_configuration.json**. **main.py** is designed to overlay 3D skeletons of humans over their RGB representaions and display the results on the screen. To execute the program, user has to input `python main.py <mode> <path_to_file>` in the command prompt. The program supports two modes: `record` and `offline`, which can be used to record a video or process a pre-recorded data, repsectively. As for `<path_to_file>` is used to assign the location to store the data or retrieve the pre-recorded video, depending on the `<mode>` chosen.

Another important file in the directory is **record.py**, which is intended to record new videos. Users can use this program by typing `python record.py <path_to_file>`, where `<path_to_file>` is the destination to store the recorded data. We purposefully design a module for this function to save computational power while recording. Even though **main.py** also supports recording, it is intended to demonstrate the overlapping of 3D skeletons and RGB images. **record.py** supports recording without laying 3D skeletons on RGB images, which is less computationally intensive.

**id.py** is used to generate subjects' biometric features frame by frame for consistently labeling each skeleton with an ID. Azure Kinect SDK and pyKinect provide body
tracking ID of each skeleton dynamically, meaning that the IDs for skeletons are different across sessions. To label each skeleton consistently across sessions, we
store three biometric features of each skeleton in a numpy array frame by frame, including the length of upper body, the length of right arm, and the length of the left
leg. The dimension of the 3D array is #subjects x #features x #frames, where the row number is also the ID assigned to the subject. With the 3D biometric array, we can determine the assigned ID of the subject by calculating the Frobenious norm between the biometric features of the subject of that frame and those of the corresponding frame in the biometric array. The row number of the smallest Frobenious norm will be the ID of the subject.To run the program, user has to type in `python id.py <#subjects> <path_to_file>` in the command prompt, where `<#subjects>` is the number of subjects present in the video and `<path_to_file>` is the path to the video to be analyzed. Note, we need to run **id.py** to extract the biometric array before running main.py to get consistent IDs.

**helper.py** includes helper functions to help consistently label the ID of each subject.

As for **device_configuration.json**, it documents the parameters required to create videos that can generate 3D skeletons. Both **main.py** and **reocrd.py** retrieves the device configuration parameters from this file.

## Acknowledgement
This repository uses and adapts code from [pyKinectAzure](https://github.com/ibaiGorordo/pyKinectAzure/tree/master).
