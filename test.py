import cv2 as cv

img = cv.imread('/home/muhammad-ali/github/AMAP/data/test_results/2_result.png')
img = cv.resize(img, (1024,1024))

cv.imwrite('/home/muhammad-ali/Downloads/r.jpg', img)