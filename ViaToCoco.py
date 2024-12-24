import json
from shapely.geometry import Polygon

def via_to_coco(via_path: str, coco_path: str):
    """
    assumes that img_height, img_width to be 4096
    assumes that obj types are only star; edge, hard or both
    takes via_path where the json file of via annotator is stored
    saves into coco_path where the json of coco format will be stored
    """

    def calculate_polygon_area(contour):
        polygon = Polygon([(contour[i], contour[i + 1]) for i in range(0, len(contour), 2)])
        return polygon.area

    def categorize(label: dict):
        if len(label['av']) == 0:
            return 1
        if label['av']['1'] == '':
            return 1
        if label['av']['1'] == '0':
            return 2
        if label['av']['1'] == '0,1':
            return 2
        if label['av']['1'] == '1':
            return 3
        if label['av']['1'] == '1,0':
            return 3


    rough = json.load(open(via_path))
    via = rough['metadata']


    coco_format = {
        "info": {'description': 'my_project'},
        "images": [],
        "annotations": [],
        "categories": [{"id": 1, "name": "star"}, {"id": 2, "name": "edge"}, {"id": 3, "name": "overlap"}],
    }

    for key, value in rough['file'].items():
        coco_format['images'] += [{"id": int(value['fid']), "file_name": value['fname'], "height": 4096, "width": 4096}]

    for i, key in enumerate(via.keys()):
        x_coords = via[key]['xy'][1::2]
        y_coords = via[key]['xy'][2::2]
        x_min, y_min = min(x_coords), min(y_coords)
        width, height = max(x_coords) - x_min, max(y_coords) - y_min

        area = calculate_polygon_area(via[key]['xy'][1:])

        coco_format["annotations"].append({
            "id": i,
            "image_id": int(via[key]['vid']),
            "category_id": categorize(via[key]),
            "segmentation": [via[key]['xy'][1:]],
            "bbox": [x_min, y_min, width, height],
            "area": area,
            "iscrowd": 0,
        })

    with open(coco_path, 'w') as f:
        json.dump(coco_format, f)

    return

via_path = '/home/muhammad-ali/github/AMAP/semantic_segmentation/testing.json'
coco_path = '/home/muhammad-ali/github/AMAP/coco.json'
# via_to_coco(via_path, coco_path)

