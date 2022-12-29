import tensorflow as tf
from utils.preprocessing import padding
from utils.loss import WeightedBinaryCrossEntropy
import warnings
import numpy as np
import os
from utils.inverter import invert
warnings.filterwarnings('ignore')


def loadModel():
    model = tf.keras.models.load_model('out/', custom_objects={'WeightedBinaryCrossEntropy':WeightedBinaryCrossEntropy}, compile=False)
    return model


def get_scores():
    model = loadModel()
    arr = []
    for image in os.listdir('uploads/'):
        path = f'uploads/{image}'
        image = tf.keras.utils.load_img(path) # Random image import
        input_arr = tf.keras.utils.img_to_array(image)
        input_arr = invert(input_arr)
        input_arr = padding(input_arr)

        arr.append(input_arr)
    arr = np.array(arr)
    scores = np.array(model.predict(arr))
    return scores.mean(axis=0)[0]

if __name__ == "__main__":
    print(get_scores())
