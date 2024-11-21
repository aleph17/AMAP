import cv2 as cv
import matplotlib.pyplot as plt
import skimage as ski
import numpy as np


img = cv.imread(r"/home/muhammad-ali/datasets/FL_Dataset/annotation_ready/52.jpg")
image = cv.cvtColor(img, cv.COLOR_BGR2RGB)

resized = cv.resize(img, (1000,1000), interpolation = cv.INTER_AREA)
gray = ski.util.invert(cv.cvtColor(resized, cv.COLOR_BGR2GRAY))

repetition = 15
for i in range(repetition):  
    gray = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)
    if (repetition%2 == 1):
        gray = cv.erode(gray, (3,3))
canny = cv.Canny(gray, 12,175)

ret,thresh = cv.threshold(gray,60,255,cv.THRESH_BINARY_INV)
skeleton = ski.morphology.skeletonize(ski.util.invert(thresh))
# plt.imshow(skeleton, 'gray')
# plt.show()

binary_mask = (thresh // 160)*255
normal_skeleton = 255*skeleton
skeleton = 1*skeleton
thinned_partial = 1*(ski.morphology.thin(ski.util.invert(binary_mask), max_num_iter=20))
normal_thinned = thinned_partial*255


dx = [-1,0,1,1,1,0,-1,-1]
dy = [-1,-1,-1,0,1,1,1,0]
for x in range(1,999):
    for y in range(1,999):
        sum = 0
        for d in range(8):
            sum += normal_thinned[x+dx[d]][y+dy[d]]
        if sum <3*255:
            normal_thinned[x][y] = 0    

# plt.imshow(normal_thinned, 'gray')
# plt.show()


dx = [-1,0,1,1,1,0,-1,-1]
dy = [-1,-1,-1,0,1,1,1,0]
for x in range(1,999):
    for y in range(1,999):
        sum = 0
        for d in range(8):
            sum += normal_thinned[x+dx[d]][y+dy[d]]
        if sum <3*255:
            normal_thinned[x][y] = 0    
plt.imshow(normal_thinned, 'gray')


cores = normal_thinned
lines = thinned_partial*255 - normal_thinned
lines[900:1000][0:200] = 0

# plt.imshow(lines, 'gray')
# plt.show()

lines = lines.astype(np.uint8)
dilated = lines.copy()
dilated = cv.dilate(dilated, (7,7))
contours, hierarchy = cv.findContours(dilated,  
    cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) 

# plt.imshow(dilated, 'gray')
# plt.show()

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

# plt.imshow(out, 'gray')
# plt.show()

zeros = np.zeros((1000,1000,3))
zeros[:,:,1] = out
result = resized - zeros.astype(int)
plt.imshow(result)
plt.show()