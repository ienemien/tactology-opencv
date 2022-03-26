import cv2

image = cv2.imread('C://projects//tactology-lab//opencv-probeersels//ink.jpg')
B, G, R = cv2.split(image)
# Corresponding channels are seperated

cv2.imshow("original", image)
cv2.waitKey(0)

cv2.imshow("blue", B)
cv2.waitKey(0)

cv2.imshow("Green", G)
cv2.waitKey(0)

cv2.imshow("red", R)
cv2.waitKey(0)

cv2.destroyAllWindows()