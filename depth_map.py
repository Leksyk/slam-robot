# OpenCV "Hello World" application. Displays depth map.
# from the first connected video device.
import sys
import cv2
import cv2.cv as cv

import numpy as np
import numpy.ma as ma

GRAYSCALE = [0.299, 0.587, 0.114]
DEVICE_L_IDX = 0
DEVICE_R_IDX = 1
DEVICE_DISTANCE = 124
FIELD_VIEW = 20.2 * math.pi / 180

def rgb2gray(rgb):
  return np.dot(rgb[:,:,0], GRAYSCALE[0]).astype(np.uint8) + np.dot(rgb[:,:,1], GRAYSCALE[1]).astype(np.uint8) + np.dot(rgb[:,:,2], GRAYSCALE[2]).astype(np.uint8)

def desparity2distance(left_x, width, desparity):
  right_x = deparity + left_x
  right_alpha = right_x / width * FIELD_VIEW
  left_alpha = left_x / width * FIELD_VIEW
  return 1/(S * math.tan(FIELD_VIEW/2 + math.pi/2 - left_alpha)) + 1/(S * math.tan(right_alpha + math.pi/2 - FILED_VIEW/2))

def main(unused_argv):
  
  font = cv2.FONT_HERSHEY_SIMPLEX
  WIDTH = 640
  HEIGHT = 480
  
  cap_l = cv2.VideoCapture(DEVICE_L_IDX)
  cap_l.set(cv.CV_CAP_PROP_FRAME_WIDTH,WIDTH)
  cap_l.set(cv.CV_CAP_PROP_FRAME_HEIGHT,HEIGHT)
  cap_r = cv2.VideoCapture(DEVICE_R_IDX)
  cap_r.set(cv.CV_CAP_PROP_FRAME_WIDTH,WIDTH)
  cap_r.set(cv.CV_CAP_PROP_FRAME_HEIGHT,HEIGHT)
  #stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET, ndisparities=320, SADWindowSize=63)
  stereo = cv2.StereoSGBM(0, 160, 11)
  while True:
    # frame type is uint8 and size (720, 1280, 3).
    ret, frame_l = cap_l.read()
    ret, frame_r = cap_r.read()

    gray_img_l = rgb2gray(frame_l)
    gray_img_r = rgb2gray(frame_r)

    gray_img_r = np.fliplr(np.flipud(gray_img_r))

    # depth map
    disparity = stereo.compute(gray_img_l, gray_img_r)
    #disparity = 255 * (disparity + np.min(disparity)) / (np.max(disparity) - np.min(disparity))
    print disparity

    cv2.putText(gray_img_l, 'Press q to quit', (0,gray_img_l.shape[0]-10), font,
        fontScale=1, color=(255, 255, 255), thickness=2)
    cv2.imshow('left', gray_img_l)
    cv2.imshow('right', gray_img_r)

    cv2.imshow('depth_map', disparity)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap_l.release()
  cap_r.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  main(sys.argv)
