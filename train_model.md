1. as in the run_socket.txt copy the path for meta_landmark_process.py inside gestures folder
2. python [meta_landmark_process.py_path from step 2] --mode 1 --label (label of your choice)
3. in the file new_keypoint_classifier_label.csv inside folder gestures/model/keypoint_classifier/, add the name for the new gesture in a new line
4. go to colab keypoint_classification_EN.ipynb, upload the updated gestures/model/keypoint_classifier/new_keypoint.csv
5. run the notebook and download the generated keypoint_classifier.tflite
6. replace gestures/model/keypoint_classifier/keypoint_classifier.tflite with the downloaded version
