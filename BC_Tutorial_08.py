import cv2
import numpy as np

# drawing helper variables
# thickness
thick = 10
thin = 3

# color
blue = (255, 0, 0)
red = (0, 0, 255)
green = (20, 200, 20)
black = (0, 0, 0)


def click_frame(event, x, y, flags, param):
    # grab references to the global variables
    global clicked_points
    # if the left mouse button was clicked, add the point to the source array
    if event == cv2.EVENT_LBUTTONDOWN:
        pos = len(clicked_points)
        if (pos == 0):
            clicked_points = [(x, y)]
        else:
            clicked_points.append((x, y))
            
clicked_points = []
img_color = cv2.imread('BildComp-SoSe2022/images/IMG_3232.JPEG', cv2.IMREAD_COLOR)

new_width = 640
new_height = 480
new_size = (new_width, new_height)
img_color = cv2.resize(img_color, new_size)


title = "title"
cv2.namedWindow(title, cv2.WINDOW_FREERATIO)
cv2.setMouseCallback(title, click_frame)
print('Press q to close the window.')

while True: 
    i = 0
    c_parameters = []
    points = []
    for c in clicked_points:
        cv2.circle(img_color, c, 4, (0, 255, 0), 2)
        i+= 1
        c_parameters.append(c)
        if i == 2:
            img = cv2.arrowedLine(img_color, c_parameters[0], c_parameters[1], blue, thin)
            a = np.array([c_parameters[0][0], c_parameters[0][1],1])
            b = np.array([c_parameters[1][0], c_parameters[1][1],1])
            crossed = np.cross(np.array([c_parameters[0][0], c_parameters[0][1],1]), np.array([c_parameters[1][0], c_parameters[1][1],1]))
            points.append(crossed)
            c_parameters = []
            i = 0
    if len(clicked_points) == 4:
        intercept = np.cross(points[0], points[1])
        intercept = intercept / intercept[2]
        print(intercept)
        cv2.circle(img_color, (intercept[0], intercept[1]), 4, (0, 255, 0), 2)
    cv2.imshow(title, img_color)
    if cv2.waitKey(10) == ord('q'):
        break

cv2.destroyAllWindows()
