import cv2
from pathlib import Path
import numpy as np

def path2id(videoPath):
    videoInfo = videoPath.name.split('.')
    if len(videoInfo)<1:
        return False, False
    elif not videoInfo[1] in ['mp4']:
        return False, False
    else:
        return True, videoInfo[0]

def make_landmark(videoPath, landmarkPath):
    cap = cv2.VideoCapture(videoPath)
    frames = []
    ret, frame = cap.read()
    while ret:
        frames.append(frame)
        ret, frame = cap.read()
    print(len(frames))
    print(frames[0].shape)
    y = model(frames)
    np.save(landmarkPath, y)


dataDir = Path('data')
landmarkDir = Path('landmark')

for videoPath in dataDir.iterdir():
    isVideo, videoId = path2id(videoPath)
    if not isVideo:
        print('{} is not video ?'.format(videoPath))
        continue
    landmarkPath = landmarkDir / (videoId + '.npy')
    if not landmarkPath.is_file():
        make_landmark(str(videoPath), str(landmarkPath))
        print('landmark -> {}'.format(landmarkPath))
    else:
        print('{} is already made'.format(landmarkPath))