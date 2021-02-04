import eel
import os
import numpy as np
from matplotlib import pyplot as plt
import uuid
import cv2
import model

id = 'unknown'
videoPath = ''
isValid = False
landmark = np.array([])
k = 0.00001
scoreLog = []
lmLog = []
resultDir = 'unknown'
mirror = True
size = ()

@eel.expose
def select_dance(_id):
    global id, videoPath, isValid, scoreLog
    id = _id
    videoPath = 'data/{}.mp4'.format(id)
    if os.path.isfile(videoPath):
        isValid = True
        scoreLog = []
        return '../data/{}.mp4'.format(id)
    else:
        isValid =False
        return 'error'

@eel.expose
def load_landmark():
    global isValid, landmark
    if isValid:
        landmark = np.load('landmark/{}.npy'.format(id))

@eel.expose
def disp_score(t):
    global landmark, scoreLog, lmLog, cap
    ret, frame = cap.read()
    if not ret:
        return 'error'
    if mirror:
        frame = frame[:,::-1]
    # y = model(frame)
    # lm_cam = np.zeros(18,2)
    # for key in y:
    #     lm_cam[key,:] = y[key]
    lm_cam = np.random.randn(18,2)
    lm_cam = opt(lm_cam, lm_video)
    is_point1, lm_video = landmark[:,t]
    if not is_point1:
        return 'error'
    s = score(lm_cam,lm_video)
    lmLog.append(lm_cam)
    scoreLog.append(s)
    return {'score':'{:.3f}'.format(s), 'landmarks':lm_cam.tolist()}

def opt(a, b):
    if a[1,0]==0, b[1,0]==0:
        return False, False
    da = a-a[1,:]
    db = b-b[1,:]
    p = np.sum((db[[8,11],:])**2) / np.sum((da[[8,11],:])**2)
    return da*p+b[1,:]
    

def score(a,b):
    global k
    L2 = np.linalg.norm(a-b)
    s = np.exp(-L2*k)*100
    return s

@eel.expose
def result():
    global resultDir
    plt.figure(figsize=(20,5))
    plt.plot(scoreLog)
    resultDir = 'result/{}_{}/'.format(id,str(uuid.uuid4()))
    while True:
        try:
            os.mkdir(resultDir)
        except:
            resultDir = 'result/{}_{}/'.format(id,str(uuid.uuid4()))
        else:
            break
    figPath = os.path.join(resultDir,'score_log.png')
    plt.savefig(figPath)
    return {'last_score':'{:.3f}'.format(np.mean(scoreLog)), 'figPath':figPath, 'movement':'100'}


@eel.expose
def save():
    global lmLog
    np.save(os.path.join(resultDir, np.array(lmLog)))
    return 1


eel.init("web")
eel.start("select.html", port=8000)
cap = cv2.VideoCapture(0)