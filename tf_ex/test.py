import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import pathlib
data_dir = pathlib.Path(os.path.join(os.environ['HOME'],'tmp','chanel_photo'))

def clean_filename(data_dir):
    for x in data_dir.iterdir():
        if x.is_dir():
            print(x, len(list(x.glob('*.jpeg'))))
            for cn_imgs, y in enumerate(x.iterdir()):
                if y.suffix == '.jpeg':
                    y.rename(os.path.join(y.parent, f'image_{cn_imgs:2d}.jpeg'))

chanel_classics = list(data_dir.glob('chanel_classic/*'))
#PIL.Image.open(str(chanel_classics[222]))


batch_size = 32
img_height = 180
img_width = 180

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

