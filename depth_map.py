# OpenCV "Hello World" application. Displays Canny edge detection output
# from the first connected video device.
import sys
import cv2

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

GRAYSCALE = [0.299, 0.587, 0.114]
DEVICE_L_IDX = 0
DEVICE_R_IDX = 1

def rgb2gray(rgb):
  return np.dot(rgb[...,...,0], GRAYSCALE[0]).astype(np.uint8) + np.dot(rgb[...,...,1], GRAYSCALE[1]).astype(np.uint8) + np.dot(rgb[...,...,2], GRAYSCALE[2]).astype(np.uint8)

def compress_color(c):
  bit1 = np.right_shift(np.right_shift(np.bitwise_and(c, 0b11110000), 7), 1)
  bit2 = np.right_shift(np.bitwise_and(c, 0b00001111), 3)
  return np.bitwise_or(bit1,bit2)

def compress_image(img):
  """convert image from size (m,n,3) to (m,n,1). 3rd dimension from 24 bits to 8 bits"""
  r = np.left_shift(compress_color(img[..., ..., 0]), 4)
  g = np.left_shift(compress_color(img[..., ..., 1]), 2)
  b = compress_color(img[..., ..., 2])
  print r
  print g
  print b
  out  = np.bitwise_or(np.bitwise_or(r, g),b)
  return out 

def main(unused_argv):
  
  font = cv2.FONT_HERSHEY_SIMPLEX
  
  cap_l = cv2.VideoCapture(DEVICE_L_IDX)
  cap_r = cv2.VideoCapture(DEVICE_R_IDX)

  while True:
    # frame type is uint8 and size (720, 1280, 3).
    ret, frame_l = cap_l.read()
    ret, frame_r = cap_r.read()
       
    gray_img_l = rgb2gray(frame_l)
    gray_img_r = rgb2gray(frame_r)

    cv2.putText(gray_img_l, 'Press q to quit', (0,gray_img.shape[0]-10), font,
        fontScale=1, color=(255, 255, 255), thickness=2)
    cv2.imshow('left', gray_img_l)
    cv2.imshow('right', gray_img_r)
    
    # depth map
    stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET, ndisparities=16, SADWindowSize=15)
    disparity = stereo.compute(gray_img_l, gray_img_r)
    cv2.imshow('depth_map', disparity)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap_l.release()
  cap_r.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  main(sys.argv)
