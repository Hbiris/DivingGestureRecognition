import sys
import numpy as np
import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque
import socket
from time import sleep
import os
import ast

import cv2 as cv
import numpy as np
import mediapipe as mp

from utils import CvFpsCalc
from model import KeyPointClassifier
from model import PointHistoryClassifier

#landmarks
LANDMARK_PARMS_NUM = 26
LANDMARK_DIM_NUM = 3
#tcp
host = '127.0.0.1' 
port = 5005
DETAIL_PRINT_MODE = False #debug log
 #main mode select
CLASSIFY_MODE = 0
RECORD_MODE = 1
# record path select
RECORD_CSV_PATH = r'C:\Users\irisbian\divinghandrecognition\Plugins\PythonScripts\newGesture.csv'
RECORD_INPUT_PATH = r'C:\Users\irisbian\divinghandrecognition\newGestureQuestion.txt'

# classify path
CLASSIFY_LABEL_CSV_PATH = r'C:\Users\irisbian\divinghandrecognition\gestures\model\keypoint_classifier\new_keypoint_classifier_label.csv'





class Landmark:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Landmark_2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def flatToLandmark(flat_list):
    # Convert into a list of Landmark objects
    landmark_list = []
    for i in range(0, len(flat_list), 3):
        x, y, z = flat_list[i:i+3]
        landmark_list.append(Landmark(x, y, z))
    return landmark_list

# === Read stdin ===
# def fetch_landmarks(data):
#     try:
#         raw_input = data.strip()
#         input_vector = list(map(float, raw_input.split(",")))

#         if len(input_vector) != LANDMARK_PARMS_NUM * LANDMARK_DIM_NUM:
#             raise ValueError("Expected ",  LANDMARK_PARMS_NUM * LANDMARK_DIM_NUM," comma-separated values for 3D landmarks.")

#         if(DETAIL_PRINT_MODE): 
#             print("✅ input:", input_vector)
#         landmark_list = flatToLandmark(input_vector)
#         return landmark_list


#     except Exception as e:
#         print("❌ Error:", e)
#         sys.exit(1)

def fetch_landmarks(data):
    try:
        input_vector = np.frombuffer(data, dtype=np.float32).tolist()

        if len(input_vector) != 78:
            raise ValueError("Expected 78 comma-separated values for 26 3D landmarks.")

        if(DETAIL_PRINT_MODE): 
            print("✅ input:", input_vector)
        landmark_list = flatToLandmark(input_vector)
        return landmark_list


    except Exception as e:
        print("❌ Error:", e)
        sys.exit(1)

def record(number):
    input_path = RECORD_INPUT_PATH
    csv_path = RECORD_CSV_PATH
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(input_path, 'r', encoding='utf-16') as f_in, open(csv_path, 'a', newline="") as f_out:
        writer = csv.writer(f_out)

        for line in f_in:
            try:
                # Parse string as list of (x, y, z) tuples
                points = ast.literal_eval(line.strip())
            except Exception as e:
                print("❌ Skipped line (parse error):", line)
                continue

            if len(points) != LANDMARK_PARMS_NUM:
                print("❌ Skipped line (wrong number of landmarks):", len(points))
                continue

            # Extract only x and y
            landmarks = [Landmark_2D(x, y) for x, y, z in points]

            raw_landmarks = calc_landmark_list(landmarks)
            landmark_list = pre_process_landmark(raw_landmarks)

            writer.writerow([number, *landmark_list])

def classify():
    # Model load #############################################################
    keypoint_classifier = KeyPointClassifier()
    # Read labels ###########################################################
    with open(CLASSIFY_LABEL_CSV_PATH, 'r',  newline='',
              encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]
    print("✅ read labels:",keypoint_classifier_labels)

    # TCP server setup #######################################################
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"📡 TCP landmark server listening on {host}:{port}...")
        while True:
            conn, addr = s.accept()
            with conn:
                if(DETAIL_PRINT_MODE): 
                    print(f"🔗 Connection from {addr}")
                while True:
                    # 26 * 3 * 4 (np.float32 is 4 byte) = 252
                    data = conn.recv(312)
                    if not data:
                        break
                    if(DETAIL_PRINT_MODE): 
                        print("📥 Received data:", data)
                    try:
                        #Fetch input landmarks (x,y,z)
                        hand_landmarks = fetch_landmarks(data)
                        # Landmark calculation
                        landmark_list = calc_landmark_list(hand_landmarks)

                        # Conversion to relative coordinates / normalized coordinates
                        pre_processed_landmark_list = pre_process_landmark(
                            landmark_list)
                        
                        if(DETAIL_PRINT_MODE):
                            print("✅ pre_processed_landmark_list:", pre_processed_landmark_list)

                        hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                        print("✅ classification: hand_sign_id ", hand_sign_id)
                        result = keypoint_classifier_labels[hand_sign_id]
                        conn.sendall(result.encode('utf-8'))
                    except Exception as e:
                        print("❌ Error processing landmarks:", e)


def calc_landmark_list(landmarks):
    image_width, image_height = 1,1

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks):
        landmark_x = landmark.x * image_width
        landmark_y = landmark.y * image_height
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=int, default=CLASSIFY_MODE, help='0: classify, 1: record to CSV, default classify')
    parser.add_argument('--label', type=int, default=0, help='Label number to record if in record mode, default 0')
    args = parser.parse_args()

    mode = args.mode
    label = args.label

    if mode == RECORD_MODE:
        print("📁 RECORD_MODE: Recording landmarks to CSV")
        record(label)
    else:
        print("📡 CLASSIFY_MODE: Classifying landmarks over TCP")
        classify()

if __name__ == '__main__':
    main()