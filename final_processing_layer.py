import cv2 as cv
import matplotlib.pyplot as plt
import skimage as ski
import numpy as np
from scipy.ndimage import convolve

def imshow(img):
    plt.imshow(img, 'gray')
    plt.show()

def line_eraser(image):
    kernel = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])
    neighbor_sum = convolve(image, kernel, mode='constant', cval=0)
    image[neighbor_sum < 3 * 255] = 0
    return image


img = cv.imread(r"/home/muhammad-ali/datasets/FL_Dataset/annotation_ready/52.jpg")
image = cv.cvtColor(img, cv.COLOR_BGR2RGB)

resized = cv.resize(img, (1000,1000), interpolation = cv.INTER_AREA)
gray = ski.util.invert(cv.cvtColor(resized, cv.COLOR_BGR2GRAY))

repetition = 10
for i in range(repetition):  
    gray = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)
    if i%2 == 1:
        gray = cv.erode(gray, (3,3))
canny = cv.Canny(gray, 12,175)

ret,thresh = cv.threshold(gray,85,255,cv.THRESH_BINARY_INV)
"""thresholding is causing problems. once detectron gives outputs it shouldn't be a problem"""
skeleton = ski.morphology.skeletonize(ski.util.invert(thresh))


binary_mask = (thresh // 160)*255
normal_skeleton = 255*skeleton
skeleton = 1*skeleton
thinned_partial = 1*(ski.morphology.thin(ski.util.invert(binary_mask), max_num_iter=20))
normal_thinned = line_eraser(thinned_partial*255)

lines = thinned_partial*255 - normal_thinned
lines[900:1000][0:200] = 0

lines = lines.astype(np.uint8)
dilated = lines.copy()
dilated = cv.dilate(dilated, (7,7))
contours, hierarchy = cv.findContours(dilated,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


aprx = []
size = []
out = np.zeros((1000,1000), np.int8)

for i in range(len(contours)):
    length = cv.arcLength(contours[i],0)
    aprx.append(cv.approxPolyDP(contours[i],20, True))
    size.append(length)
    cv.putText(out,str(round(length)),contours[i][0][0],2,1,1,2) # 1,2) first is the color

for i in range(len(aprx)):
    (x,y), radius = cv.minEnclosingCircle(aprx[i])
    length = cv.arcLength(aprx[i],0)
    cv.putText(out,str(round(length)),(int(x)+3,int(y)+3),1,2,255,2)
out  = cv.drawContours(out, aprx,-1,255,3)


zeros = np.zeros((1000,1000,3))
zeros[:,:,1] = out
result = resized - zeros.astype(int)
cv.imwrite('/home/muhammad-ali/Downloads/line.jpg', result)