import os
import cv2
from ultralytics import YOLO


frame_size = 640

def load_model(model_path):
    return YOLO(model_path)

def preprocess(frame):
    frame = cv2.resize(frame,(frame_size,frame_size))
    return frame