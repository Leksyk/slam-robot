# OpenCV "Hello World" application. Displays Canny edge detection output
# from the first connected video device.
import sys
import gflags
import cv2


FLAGS = gflags.FLAGS
gflags.DEFINE_integer('capture_device_index', 0, 'Capture device index')


def main(unused_argv):
  window_name = 'Hello'
  font = cv2.FONT_HERSHEY_SIMPLEX
  cap = cv2.VideoCapture(FLAGS.capture_device_index)

  while True:
    ret, frame = cap.read()
    out = cv2.Canny(frame, 100, 200)
    cv2.putText(out, 'Press q to quit', (0,frame.shape[0]-10), font,
        fontScale=1, color=(255, 255, 255), thickness=2)
    cv2.imshow(window_name, out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  main(FLAGS(sys.argv))
