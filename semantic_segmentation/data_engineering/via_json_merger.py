import json
import os

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
        labels[value['vid']] += [key]
    return labels

def new_vid_gen(new: dict)->dict:
    new_vid = {}
    for key,value in new['file'].items():
         new_vid[key] = value['fname']
    return(new_vid)

def dumper(vid_tran, labels, new_vid,fily, destination):
    dst_json = json.load(open(destination))
    for key, value in new_vid.items():
        if value in vid_tran.keys():
            aim_labels = labels[vid_tran[value]]
            for i in aim_labels:
                if len(fily['metadata'][i]['xy']) != 0:
                    dst_json['metadata'][i] = fily['metadata'][i]
                    dst_json['metadata'][i]['vid'] = key
    with open(destination, 'w') as f:
        json.dump(dst_json, f)

def main():
    source = 'FL_project.json'
    destination = 'new_fl.json'

    src_json = json.load(open(source))
    dst_json = json.load(open(destination))

    vid = vid_gen(src_json)
    vid_tran = vid_tr_gen(vid)
    labels = label_gen(vid, src_json)
    new_vid = new_vid_gen(dst_json)

    dumper(vid_tran, labels, new_vid, src_json, destination)
    return
