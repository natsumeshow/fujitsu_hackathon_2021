import eel
import os
import numpy as np
from matplotlib import pyplot as plt
import uuid
import cv2
import math
import time
import datetime
from model import model
import tensorflow as tf
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path


w, h = 432, 368
e = TfPoseEstimator(get_graph_path('cmu'), target_size=(w, h), tf_config=tf.ConfigProto(log_device_placement=True))
k = 0.00002

id = 'unknown'
videoPath = ''
isValid = False
landmark = np.array([])
k = 0.002
scoreLog = []
lmLog = []
resultDir = 'unknown'
mirror = True
fps = 30
cam_resize_before = None
vid_resize_before = None
y_log = []
sum_mov = 0

@eel.expose
def select_dance(_id):
    global id, videoPath, isValid, scoreLog, cap, landmark, fps
    id = _id
    videoPath = 'data/{}.mp4'.format(id)
    if os.path.isfile(videoPath):
        fps = cv2.VideoCapture(videoPath).get(cv2.CAP_PROP_FPS)
        isValid = True
        scoreLog = []
        cap = cv2.VideoCapture(0)
        # ret, frame = cap.read()
        # print(ret)
        landmark = np.load('landmark/{}.npy'.format(id))
        return '../data/{}.mp4'.format(id)
    else:
        isValid =False
        return 'error'


@eel.expose
def disp_score(t):
    print(1)
    global landmark, scoreLog, lmLog, cap, cam_resize_before, vid_resize_before, sum_mov
    if t == -1:
        time.sleep(0.3)
        print(-1)
        return {'isPlaying': False}
    
    t = math.floor(t*fps)
    if t >= len(landmark):
        print("over")
        return {'isPlaying': False}
    ret, frame = cap.read()
    # print(ret)
    # print(frame)
    # frame = cv2.resize(frame, (w,h), interpolation = cv2.INTER_LINER)
    if not ret:
        print('not ret')
        return {'isPlaying': False}
    if mirror:
        frame = frame[:,::-1]
    y = model(frame,e,(False,False),4)
    lm_cam = np.zeros([18,2])
    for key in y:
        lm_cam[key,:] = y[key]
    lm_video = landmark[t,:,:]
    if lm_cam[1,0]==0:
        print('not point1')
        return {'isPlaying': False}
    cam_shift, cam_resize = opt_param(lm_cam)
    vid_shift, vid_resize = opt_param(lm_video)

    sum_mov += movement(y, y_log[-1], cam_resize) if len(y_log)>0 else 0
    y_log.append(y)
    print(y)

    if cam_resize_before != None:
        if cam_resize==-1:
            cam_resize = cam_resize_before
        else:
            cam_resize = cam_resize_before * 0.1 + cam_resize * 0.9

    if vid_resize_before != None:
        if vid_resize==-1:
            vid_resize = vid_resize_before
        else:
            vid_resize = vid_resize_before * 0.1 + vid_resize * 0.9

    # if cam_resize != 0 and vid_resize != 0:
        # lm_cam = (lm_cam - cam_shift) * (vid_resize / cam_resize) + vid_shift
        # lm_cam = (lm_cam - cam_shift) + vid_shift


    out_landmark = {i: ((lm_cam[i,:]*1.74).tolist() if i in y.keys() else [-1,-1]) for i in range(14)}

    s = score(lm_cam,lm_video)
    lmLog.append(lm_cam)
    scoreLog.append(s)
    output = {'isPlaying': True, 'score':'{:.3f}'.format(s), 'landmark':out_landmark}
    print(output)
    return output

def opt_param(lm):
    if lm[1,0]==0:
        return 0, 0
    elif lm[8,0]==0 and lm[11,0]==0:
        return lm[1,:], 0
    else:
        if lm[8,0]==0:
            return lm[1,:], np.sum((lm[11,:]-lm[1,:])**2)
        elif lm[11,0]==0:
            return lm[1,:], np.sum((lm[8,:]-lm[1,:])**2)
        else:
            return lm[1,:], np.sum((lm[[8,11],:]-lm[1,:])**2)/np.sqrt(2)


def opt(a, b):
    if a[1,0]==0 and b[1,0]==0:
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
    print("start result()")
    global resultDir, scoreLog, sum_mov
    plt.figure(figsize=(20,5))
    plt.plot(scoreLog)
    plt.ylim(0,100)
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
    print(sum_mov)
    output = {'last_score':'{:.3f}'.format(np.mean(scoreLog)), 'figPath':'../'+figPath, 'movement':'{:4d}'.format(math.floor(sum_mov))}
    print(output)
    sum_mov=0
    scoreLog=[]
    return output


@eel.expose
def save():
    global lmLog
    np.save(os.path.join(resultDir, np.array(lmLog)))
    return 1


def movement(y1, y2, size):
    interkeys = set(y1.keys()).intersection(y2.keys())
    sum = 0
    for i in interkeys:
        sum += (y1[i][0]-y2[i][0])**2
        sum += (y1[i][1]-y2[i][1])**2
    mov = sum/len(interkeys) if len(interkeys)!=0 else 0
    return np.sqrt((mov/size**2))*100


eel.init("./")
eel.start("web/select.html", port=8000)