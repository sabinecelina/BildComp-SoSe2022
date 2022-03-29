import numpy as np
import cv2

# TODO open a video file

file = 'BildComp-SoSe2022/videos/hello_UH.m4v'
cap = cv2.VideoCapture(file)

# TODO get camera image parameters from get()

height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
codec = cap.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT)
frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

print("height : ", str(height))
print("width: ", width)
print("codec: ", codec)
print("frames: ", frames)

# # TODO start a loop

while(True):
#     # TODO (in loop) read one video frame
    ret, frame = cap.read()
    print(ret)
#     # TODO (in loop) create four tiles of the image
#     if(ret):
#         img = np.zeros(frame.shape, np.uint8)
#         smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
#         img[:height//2, :width//2] = smaller_frame  # top left (original)
#         img[height//2:, :width//2] = cv2.flip(smaller_frame, 0)
#         img[:height//2, width//2:] = cv2.flip(smaller_frame, 1)
#         img[height//2:, width//2:] = cv2.flip(smaller_frame, -1)
#     # Display the resulting frame
#         cv2.imshow('frame', img)
      
#     # the 'q' button is set as the
#     # quitting button you may use any
#     # desired button of your choice
    if cv2.waitKey(10) == ord('q'):
        break
  
# # After the loop release the cap object
# cap.release()
# # # Destroy all the windows
# cv2.destroyAllWindows()