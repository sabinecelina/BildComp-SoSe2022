# load an image and find vanishing points
import operator
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

# load image
img = cv2.imread('images/table_bottle_01.jpg', cv2.IMREAD_COLOR)
height, width, _ = img.shape


def click_frame(event, x, y, flags, param):
    # grab references to the global variables
    global clicked_points
    # if the left mouse button was clicked, add the point to the source array
    if event == cv2.EVENT_LBUTTONDOWN:
        pos = len(clicked_points)
        if pos == 0:
            clicked_points = [(x, y)]
        else:
            clicked_points.append((x, y))


clicked_points = []


def get_window_frame(points):
    x = 0
    y = 0
    for point in points:
        if point[0] > x:
            x = point[0]
        if point[1] > y:
            y = point[1]
    print(x, y)


def calc_vanishing_point():
    vanishing_points = []
    title = "title"
    cv2.namedWindow(title, cv2.WINDOW_FREERATIO)
    cv2.setMouseCallback(title, click_frame)
    print('Press q to close the window.')
    check = True
    while check:
        i = 0
        c_parameters = []
        points = []
        for c in clicked_points:
            cv2.circle(img, c, 4, (0, 255, 0), 2)
            i += 1
            c_parameters.append(c)
            if i == 2:
                cv2.arrowedLine(img, c_parameters[0], c_parameters[1], blue, thin)
                crossed = np.cross(np.array([c_parameters[0][0], c_parameters[0][1], 1]),
                                   np.array([c_parameters[1][0], c_parameters[1][1], 1]))
                points.append(crossed)
                c_parameters = []
                i = 0
            if len(clicked_points) == 4:
                if len(points) == 2:
                    vanishing_point = np.cross(points[0], points[1])
                    vanishing_point = vanishing_point / vanishing_point[2]
                    cv2.circle(img, (int(vanishing_point[0]), int(vanishing_point[1])), 4, (0, 255, 0), 2)
                    vanishing_points.append(vanishing_point)
        cv2.imshow(title, img)
        if len(vanishing_points) == 2:
            print('lol')
        if cv2.waitKey(10) == ord('q'):
            break
        print(vanishing_points)
        # get_window_frame(vanishing_points)
    return vanishing_points


calc_vanishing_point()
cv2.destroyAllWindows()
# TODO Implement callback function that contains the whole process

# TODO Create a large image that contains the vanishing points

# TODO Draw the original image region and vanishing points in the large image

# TODO Draw the vanishing line between 

# TODO create a window for the image
