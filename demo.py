import argparse
import logging
import sys
import time
import os 
import glob
import cv2
import numpy as np

import tensorflow as tf 
from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh


img_outdir = './demo'
os.makedirs(img_outdir, exist_ok=True)

# Generate demo video 
width = 1280
height = 720
fps = 30.0

fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
video  = cv2.VideoWriter('demo.mp4', fourcc, fps, (width, height))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='tf-pose-estimation run')
	parser.add_argument('--model', type=str, default='cmu',
		help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
	parser.add_argument('--resize', type=str, default='432x368',
		help='if provided, resize images before they are processed. '
		'default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
	parser.add_argument('--resize-out-ratio', type=float, default=4.0,
		help='if provided, resize heatmaps before they are post-processed. default=1.0')

	args = parser.parse_args()

    # your image path 
	path = "/home/natsu/CTRACKER_ROOT/CTracker/test/test/demo_movie/"
	files= glob.glob(path + "*")

	use_landmark = [i for i in range(14)]


	w, h = model_wh(args.resize)
	if w == 0 or h == 0:
		e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368), tf_config=tf.ConfigProto(log_device_placement=True))
	else:
		e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h), tf_config=tf.ConfigProto(log_device_placement=True))

	Current_score = 100
	count = 1
	sum_score = 0

	for file in sorted(files) :
		image = cv2.imread(file, cv2.IMREAD_COLOR)
    	# Pose estimation
		humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4)
		img ,centers = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

		teacher = np.array([])
		user = np.array([])

		#print(centers)
		for idx in use_landmark : 	

			try :
				teacher = np.append(teacher , [centers[idx]])
				user = np.append(user , [centers[idx]])
			except : 
				teacher = np.append(teacher , [(0,0)])
				user = np.append(user , [(0,0)])

		user += np.random.randint(5)
		#print('teacher' , teacher)
		#print("user" , user)
		score = 100 - np.linalg.norm(teacher - user ) 
		Current_score = (sum_score + score) / count 
		sum_score += score
		
		print(str(count) + ": Current_score {}".format( Current_score) , score)
		outimg_file = '{}/{:05d}.jpg'.format(img_outdir, count)	

		cv2.putText(image,
					'Current score : {:.1f}'.format(Current_score) ,
						(15, 15),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
						(0, 255, 0), 4)

		cv2.imwrite(outimg_file, image)
		count += 1 
		video.write(image)