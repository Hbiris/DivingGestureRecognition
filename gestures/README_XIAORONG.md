# 安装
装新版本就可以（应该）
* mediapipe 0.8.1
* OpenCV 3.4.2 or Later
* Tensorflow 2.3.0 or Later<br>tf-nightly 2.5.0.dev or later (Only when creating a TFLite for an LSTM model)
* scikit-learn 0.23.2 or Later (Only if you want to display the confusion matrix) 
* matplotlib 3.3.2 or Later (Only if you want to display the confusion matrix)
readme里有specify他的，不过我下最新的也可以：(python 3.9.21)
matplotlib                   3.9.4
mediapipe                    0.10.21
opencv-python                4.11.0.86
scikit-learn                 1.6.1
tensorflow                   2.19.0
# 处理数据 tcp_landmark_process
    持续接受tcp传来的数据，运行keypoint_classifier识别结果
    现在为了适配mediapipe测试设定，之后可以修改的参数：
    - host = '127.0.0.1' port = 5005
    - LANDMARK_PARMS_NUM = 21
    - DETAIL_PRINT_MODE = False
    TODO: 整合进diving里的tcp script

# app.py
    python app.py
    加了一个tcp模式，识别代码后按TCP_KEY发送给tcp_landmark_process处理，来测试结果
    - TCO_SEND_KEY = 105 #i
    - host = '127.0.0.1'
    - port = 5005

# tcp_sender.py
    可以直接发送landmark手势数据来检验
    - host = '127.0.0.1'
    - port = 5005

# model/keypoint_classifier, keypoint_classification_EN.ipynb
    TODO：添加数据/label，通过keypoint_classification_EN.ipynb重新train keypoint_classifier