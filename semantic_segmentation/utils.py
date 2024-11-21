from typing import List
import matplotlib.pyplot as plt
from tensorflow.keras.utils import array_to_img
from os import path, getenv
import tensorflow as tf

# directories
root_path = '/home/muhammad-ali/github/AMAP'
img_pth = path.join(root_path, "segmentation/samples")
train_dir = path.join(root_path, "tf_record/Train")
val_dir = path.join(root_path, "tf_record/Valid")
test_dir = path.join(root_path, "tf_record/Test")
orig_train_dir = path.join(root_path, "tf_record/Original_Train")
checkpoint_filepath = 'BaseModel/checkpoint.model.keras'

#numerical stable variables
tf_global_seed = 1234
np_seed = 1234
shuffle_data_seed = 12345
INITIAL_BIAS = -1.63050504

# Hyper-parameters
AUTOTUNE = tf.data.AUTOTUNE
BUFFER_SIZE = 1024
BATCH_SIZE = 32
LEARNING_RATE = 0.0003

# The required image size.
IMG_SIZE = 256
OUTPUT_CLASSES = 2


def display(display_list: List) -> None:
    """
    [true_image,true_mask,predicted_mask] -> display
    """
    plt.figure(figsize=(15, 15))
    title = ['Input Image', 'True Mask', 'Predicted Mask']

    for idx in range(len(display_list)):
        plt.subplot(1, len(display_list), idx + 1)
        plt.title(title[idx])
        plt.imshow(array_to_img(display_list[idx]))
        plt.axis('off')
    plt.show()


def squeeze_mask(img, mask):
    return img, tf.squeeze(mask, axis=-1)

def create_mask(pred_mask):
    pred_mask = tf.math.argmax(pred_mask, axis=-1)
    pred_mask = pred_mask[..., tf.newaxis]
    return pred_mask[0]

# Instantiate an optimizer.
optimAdam = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)

