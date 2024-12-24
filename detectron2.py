import sys
import os
import torch
import detectron2
from detectron2.utils.logger import setup_logger
import numpy as np
import json
import cv2
import random
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor, DefaultTrainer
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.data.datasets import register_coco_instances
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader
import yaml
from matplotlib import pyplot as plt


def setup_detectron():
    # Install required packages
    os.system('python -m pip install pyyaml==5.1')
    os.system('git clone https://github.com/facebookresearch/detectron2')
    sys.path.insert(0, os.path.abspath('./detectron2'))


def register_datasets(train_json, train_dir, val_json, val_dir):
    register_coco_instances("my_dataset_train", {}, train_json, train_dir)
    register_coco_instances("my_dataset_val", {}, val_json, val_dir)

    return (MetadataCatalog.get("my_dataset_train"),
            DatasetCatalog.get("my_dataset_train"),
            MetadataCatalog.get("my_dataset_val"),
            DatasetCatalog.get("my_dataset_val"))


def visualize_samples(dataset_dicts, metadata, num_samples=2):
    for d in random.sample(dataset_dicts, num_samples):
        img = cv2.imread(d["file_name"])
        visualizer = Visualizer(img[:, :, ::-1], metadata=metadata, scale=0.5)
        vis = visualizer.draw_dataset_dict(d)
        plt.figure(figsize=(10, 10))
        plt.imshow(vis.get_image()[:, :, ::-1])
        plt.show()


def setup_config(output_dir, num_classes):
    cfg = get_cfg()
    cfg.OUTPUT_DIR = output_dir
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
    cfg.DATASETS.TRAIN = ("my_dataset_train",)
    cfg.DATASETS.TEST = ()
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml")
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.00025
    cfg.SOLVER.MAX_ITER = 1000
    cfg.SOLVER.STEPS = []
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 256
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = num_classes

    return cfg


def train_model(cfg):
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()

    return trainer


def save_config(cfg, config_path):
    with open(config_path, 'w') as file:
        yaml.dump(cfg, file)


def setup_predictor(cfg, model_path, thresh=0.5):
    cfg.MODEL.WEIGHTS = model_path
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = thresh
    return DefaultPredictor(cfg)


def evaluate_model(cfg, predictor):
    evaluator = COCOEvaluator("my_dataset_val", output_dir="./output")
    val_loader = build_detection_test_loader(cfg, "my_dataset_val")
    return inference_on_dataset(predictor.model, val_loader, evaluator)


def process_images(predictor, input_dir, output_dir, metadata):
    os.makedirs(output_dir, exist_ok=True)

    for image_filename in os.listdir(input_dir):
        image_path = os.path.join(input_dir, image_filename)
        image = cv2.imread(image_path)
        outputs = predictor(image)

        v = Visualizer(image[:, :, ::-1], metadata=metadata)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

        result_filename = os.path.splitext(image_filename)[0] + "_result.png"
        output_path = os.path.join(output_dir, result_filename)
        cv2.imwrite(output_path, out.get_image()[:, :, ::-1])


def main():
    # Setup paths
    train_json = "/content/drive/MyDrive/ColabNotebooks/data/train/train.json"
    train_dir = "/content/drive/MyDrive/ColabNotebooks/data/train"
    val_json = "/content/drive/MyDrive/ColabNotebooks/data/val/val.json"
    val_dir = "/content/drive/MyDrive/ColabNotebooks/data/val"
    output_dir = "/content/drive/MyDrive/ColabNotebooks/models/Detectron2_Models"

    # Setup and register datasets
    setup_detectron()
    train_metadata, train_dicts, val_metadata, val_dicts = register_datasets(
        train_json, train_dir, val_json, val_dir)

    # Visualize samples
    visualize_samples(train_dicts, train_metadata)

    # Setup and train model
    cfg = setup_config(output_dir, num_classes=3)
    trainer = train_model(cfg)

    # Save config
    save_config(cfg, os.path.join(output_dir, "config.yaml"))

    # Setup predictor and evaluate
    model_path = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    predictor = setup_predictor(cfg, model_path)
    metrics = evaluate_model(cfg, predictor)
    print("Evaluation metrics:", metrics)

    # Process test images
    test_dir = "/content/drive/MyDrive/ColabNotebooks/data/test"
    results_dir = "/content/drive/MyDrive/ColabNotebooks/data/test_results"
    process_images(predictor, test_dir, results_dir, train_metadata)


if __name__ == "__main__":
    main()