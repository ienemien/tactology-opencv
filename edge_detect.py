import cv2
import numpy as np

FILE_NAME = 'ink.jpg'
try:
	# Read image from disk.
	img = cv2.imread(FILE_NAME)

	# Canny edge detection.
	edges = cv2.Canny(img, 100, 200)

	# Write image back to disk.
	cv2.imshow('result.jpg', edges)

	cv2.waitKey(0)
	cv2.destroyAllWindows()
except IOError:
	print ('Error while reading files !!!')
