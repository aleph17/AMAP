import os
import json
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def vid_gen(fily: dict) -> dict:
    """generates a dict where {key: value} is {vid: filename}"""
    vid = {}
    for key, value in fily['file'].items():
        vid[key] = value['fname']
    return vid
def vid_tr_gen(vid: dict) -> dict:
    """generates a dict where {key: value} is {filename: vid}"""
    vid_tran = {}
    for key, value in vid.items():
        vid_tran[value] = key
    return vid_tran
def label_gen(vid: dict, fily: dict)-> dict:
    """generates a dict where {key: value} is {vid: [list of label names]}"""
    labels = {}
    for key, value in vid.items():
        labels[key] = []
    for key, value in fily['metadata'].items():
        if len(fily['metadata'][key]['xy']) != 0:
            labels[value['vid']] += [key]
    return labels

fily = json.load(open('../testing.json'))
vid = vid_gen(fily)
vid_tran = vid_tr_gen(vid)
labels = label_gen(vid, fily)

for key, value in labels.items():
    mask_dir = 'segmentation/masks/'+ f'{vid[key].split('.')[0]}'
    img_dir = 'segmentation/samples/'+ f'{vid[key].split('.')[0]}'
    img = cv.imread('images/'+f"{vid[key]}")
    for k in range(len(value)):

        label = value[k]
        target = fily['metadata'][label]['xy']
        contours = []
        x_max = -1
        y_max = -1
        x_min = 5000
        y_min = 5000
        for i in range(1, len(target), 2):
            #trimming
            x = max(target[i], 0)
            y = max(target[i+1], 0)
            x = min(x, 4096)
            y = max(y, 4096)

            #min_max
            x_max = max(x_max, x)
            y_max = max(y_max, y)
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            contours.append([x, y])
        contours = np.array(contours)

        #mask and its corresponding contours
        mask = np.zeros([y_max - y_min,x_max - x_min])
        contours -= [x_min, y_min]

        cv.drawContours(mask, [contours], -1,255, -1)
        cv.imwrite(mask_dir + f"_{k}.jpg", mask)
        cv.imwrite(img_dir + f"_{k}.jpg", img[y_min:y_max, x_min:x_max])
