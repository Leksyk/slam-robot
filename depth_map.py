# OpenCV "Hello World" application. Displays depth map.
# from the first connected video device.
import sys
import cv2
import cv2.cv as cv

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

GRAYSCALE = [0.299, 0.587, 0.114]
DEVICE_L_IDX = 0
DEVICE_R_IDX = 1

def rgb2gray(rgb):
  return np.dot(rgb[:,:,0], GRAYSCALE[0]).astype(np.uint8) + np.dot(rgb[:,:,1], GRAYSCALE[1]).astype(np.uint8) + np.dot(rgb[:,:,2], GRAYSCALE[2]).astype(np.uint8)

def main(unused_argv):
  
  font = cv2.FONT_HERSHEY_SIMPLEX
  
  cap_l = cv2.VideoCapture(DEVICE_L_IDX)
  cap_l.set(cv.CV_CAP_PROP_FRAME_WIDTH,160)
  cap_l.set(cv.CV_CAP_PROP_FRAME_HEIGHT,120)
  cap_r = cv2.VideoCapture(DEVICE_R_IDX)
  cap_r.set(cv.CV_CAP_PROP_FRAME_WIDTH,160)
  cap_r.set(cv.CV_CAP_PROP_FRAME_HEIGHT,120)
  stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET, ndisparities=16, SADWindowSize=15)
  while True:
    # frame type is uint8 and size (720, 1280, 3).
    ret, frame_l = cap_l.read()
    ret, frame_r = cap_r.read()
       
    gray_img_l = rgb2gray(frame_l)
    gray_img_r = rgb2gray(frame_r)

    cv2.putText(gray_img_l, 'Press q to quit', (0,gray_img_l.shape[0]-10), font,
        fontScale=1, color=(255, 255, 255), thickness=2)
    cv2.imshow('left', gray_img_l)
    cv2.imshow('right', gray_img_r)
    
    # depth map
    disparity = stereo.compute(gray_img_l, gray_img_l)
    cv2.imshow('depth_map', disparity)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap_l.release()
  cap_r.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  main(sys.argv)
