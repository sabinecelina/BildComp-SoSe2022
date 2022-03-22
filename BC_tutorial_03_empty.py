import code
import numpy as np
import cv2
import math
import operator


cap = cv2.VideoCapture(0)

height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
codec = cap.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT)


print("height : ", height)
print("width: ", width)
print("codec: ", codec)

cv2.namedWindow("webcam picture", cv2.WINDOW_FREERATIO)

while(True):
    # ret is a boolean that returns true if the frame is available.
    # frame is an image array vector captured based on the default frames per second defined explicitly or implicitly
    ret, frame = cap.read()
  
    if(ret):
        img = np.zeros(frame.shape, np.uint8)
        smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        img[:height//2, :width//2] = smaller_frame  # top left (original)
        img[height//2:, :width//2] = cv2.flip(smaller_frame, 0)
        img[:height//2, width//2:] = cv2.flip(smaller_frame, 1)
        img[height//2:, width//2:] = cv2.flip(smaller_frame, -1)
    # Display the resulting frame
    cv2.imshow('frame', img)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
cap.release()
# # Destroy all the windows
cv2.destroyAllWindows()

# TODO release the video capture object and window
