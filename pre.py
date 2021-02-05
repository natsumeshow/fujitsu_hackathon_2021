import cv2
from pathlib import Path
import numpy as np
from dammy import model

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
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # frames = []
    ret, frame = cap.read()
    lms = []
    while ret:
        # frames.append(frame)
        ret, frame = cap.read()
        lm = np.zeros(18,2)
        y = model(frame)
        for key in y:
            lm[key,:] = y[key]
        lms.append(lm)
    # print(len(frames))
    # print(frames[0].shape)
    np.save(landmarkPath, np.array(lms))


dataDir = Path('data')
landmarkDir = Path('landmark')
try:
    dataDir.mkdir()
except:
    None
try:
    landmarkDir.mkdir()
except:
    None

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