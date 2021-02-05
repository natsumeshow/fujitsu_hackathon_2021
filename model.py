# import argparse
# import logging
# import sys
# import time
# import os
# import glob
# import cv2
# import numpy as np

# import tensorflow as tf
from tf_pose.estimator import TfPoseEstimator
from dammy import model as dammy_model

def model(image, e, resize_to_default=(True, True), upsample_size=4):
    if e == 0:
        print('use dammy model because of unvalid e')
        return dammy_model(image, e, resize_to_default=(True, True), upsample_size=4)
    humans = e.inference(image, resize_to_default, upsample_size)
    _ ,centers = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    return centers
