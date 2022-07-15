import argparse
import cv2
import numpy as np
import random
import time
import time
from matplotlib import pyplot as plt
from pythonosc import udp_client

# range of red
RED_MIN = np.array([0, 100, 100])
RED_MAX = np.array([5, 255, 255])

# range of blue
BLUE_MIN = np.array([98, 50, 50])  # setting the blue lower limit
BLUE_MAX = np.array([139, 255, 255])  # setting the blue upper limit

# range of green
GREEN_MIN = np.array([25, 52, 72])
GREEN_MAX = np.array([102, 255, 255])

imcap = cv2.VideoCapture(0)
imcap.set(3, 640)  # set width as 640
imcap.set(4, 480)  # set height as 480

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)

    while True:
        success, img = imcap.read()  # capture frame from video

        # 1: detect shapes
        # converting image into grayscale image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        # input image, output thresh value, adaptive thresholding method, thresholding method, area value, constant c for finetuning
        threshold = cv2.adaptiveThreshold(blurred, 255,
                                          cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 6)
        # show the threshold
        cv2.imshow('threshold', threshold)

        # using a findContours() function
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        i = 0

        # list for storing names of shapes
        shapes = []
        for contour in contours:

            # here we are ignoring first counter because
            # findcontour function detects whole image as shape
            if i == 0:
                i = 1
                continue

            arc = cv2.arcLength(contour, True)
            if arc < 130:
                continue

            # cv2.approxPloyDP() function to approximate the shape
            approx = cv2.approxPolyDP(contour, 0.04 * arc, True)

            # using drawContours() function
            cv2.drawContours(img, [contour], 0, (255, 255, 255), 5)

            # finding center point of shape
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])

            # putting shape name at center of each shape
            if len(approx) == 3:
                cv2.putText(img, 'triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                shapes.append(['triangle', arc])

            elif len(approx) == 4:
                cv2.putText(img, 'rectangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                shapes.append(['rectangle', arc])

            else:
                cv2.putText(img, 'circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                shapes.append(['circle', arc])

        client.send_message('/shapes', shapes)

        # 1: detect colors
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # detect amount of red and add it to image
        redmask = cv2.inRange(hsv, RED_MIN, RED_MAX)
        red_count = np.count_nonzero(redmask)
        cv2.putText(img, 'red: ' + str(red_count), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # detect amount of green
        greenmask = cv2.inRange(hsv, GREEN_MIN, GREEN_MAX)
        greencount = np.count_nonzero(greenmask)
        cv2.putText(img, 'green: ' + str(greencount), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # detect amount of blue
        bluemask = cv2.inRange(hsv, BLUE_MIN, BLUE_MAX)
        bluecount = np.count_nonzero(bluemask)
        cv2.putText(img, 'blue: ' + str(bluecount), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # send rgb values to the music player
        new_rgb = [red_count, greencount, bluecount]
        print("sending rgb vals: " + str(new_rgb))
        client.send_message('/rgb', new_rgb)

        # displaying the image after drawing contours
        cv2.imshow('shapes', img)

        # wait a bit
        time.sleep(0.5)

        # loop will be broken when 'q' is pressed on the keyboard
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyWindow('face_detect')
