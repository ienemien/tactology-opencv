import cv2
import numpy as np

# Enable we
# '0' is default ID for builtin web cam
# for external web cam ID can be 1 or -1
imcap = cv2.VideoCapture(0)
imcap.set(3, 640)  # set width as 640
imcap.set(4, 480)  # set height as 480

# detect range of red
RED_MIN = np.array([0, 100, 100])
RED_MAX = np.array([5, 255, 255])

# range of blue
BLUE_MIN = np.array([98, 50, 50])  # setting the blue lower limit
BLUE_MAX = np.array([139, 255, 255])  # setting the blue upper limit

# range of green
GREEN_MIN = np.array([25, 52, 72])
GREEN_MAX = np.array([102, 255, 255])

while True:
    success, img = imcap.read()  # capture frame from video
    # converting image from BGR to HSV
    #get amount of blue pixels in whole image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    redmask = cv2.inRange(hsv, RED_MIN, RED_MAX)
    red_count = np.count_nonzero(redmask)

    # draw rectangle around part of image
    # params: image, (xstart, ystart), (xend, yend), (B, G, R), pixel_width
    cv2.rectangle(img, (320, 240), (340, 260), (255, 0, 0), 2)
    cv2.putText(img, 'red: ' + str(red_count), (342, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # get amount of red from part of image?
    # [xvan:xtot, yvan:ytot] vanaf linksbovenin
    middle = img[300:640, 240:480]
    hsv_mid = cv2.cvtColor(middle, cv2.COLOR_BGR2HSV)
    redmask_mid = cv2.inRange(hsv_mid, RED_MIN, RED_MAX)
    red_count_mid = np.count_nonzero(redmask_mid)
    cv2.putText(middle, 'red: ' + str(red_count_mid), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.imshow('middle', middle)

    part2 = img[100:200, 200:400]
    cv2.imshow('part2', part2)

    # show input image as well as mask
    cv2.imshow('image_window_name', img)
    cv2.imshow('mask_window_name', redmask)

    # loop will be broken when 'q' is pressed on the keyboard
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
imcap.release()
cv2.destroyAllWindows()
