import eel
import os
import numpy as np
from matplotlib import pyplot as plt
import uuid
import cv2
try:
    from model import model
except Exception as e:
    print(e)
    print("import dammy model")
    from dammy import model
try:
    from tf_pose.networks import get_graph_path
except Exception as e:
    print(e)

id = 'unknown'
videoPath = ''
isValid = False
landmark = np.array([])
k = 0.00001
scoreLog = []
lmLog = []
resultDir = 'unknown'
mirror = True
# size = ()
w, h = 432, 368
try:
	e = TfPoseEstimator(get_graph_path(model), target_size=(w, h), tf_config=tf.ConfigProto(log_device_placement=True))
except:
    e = 0

@eel.expose
def select_dance(_id):
    global id, videoPath, isValid, scoreLog, cap, landmark
    id = _id
    videoPath = 'data/{}.mp4'.format(id)
    if os.path.isfile(videoPath):
        isValid = True
        scoreLog = []
        cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
        landmark = np.load('landmark/{}.npy'.format(id))
        return '../data/{}.mp4'.format(id)
    else:
        isValid =False
        return 'error'

# @eel.expose
# def load_landmark():
#     global isValid, landmark
#     if isValid:
#         landmark = np.load('landmark/{}.npy'.format(id))

@eel.expose
def disp_score(t):
    global landmark, scoreLog, lmLog, cap
    ret, frame = cap.read()
    if not ret:
        return 'error'
    if mirror:
        frame = frame[:,::-1]
    y = model(frame,e,(True,True),4)
    lm_cam = np.zeros([18,2])
    for key in y:
        lm_cam[key,:] = y[key]
    # lm_cam = np.random.randn(18,2)
    lm_video = landmark[t,:,:]
    is_point1 = False if lm_video[1,0]==-1 else True
    lm_cam = opt(lm_cam, lm_video)
    if not is_point1:
        return 'error'
    s = score(lm_cam,lm_video)
    lmLog.append(lm_cam)
    scoreLog.append(s)
    print({'score':'{:.3f}'.format(s), 'landmark':lm_cam.tolist()[:14]})
    return {'score':'{:.3f}'.format(s), 'landmark':lm_cam.tolist()[:14]}

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
    print({'last_score':'{:.3f}'.format(30.28475), 'figPath':'../'+figPath, 'movement':'100'})
    # return {'last_score':'{:.3f}'.format(np.mean(scoreLog)), 'figPath':'../'+figPath, 'movement':'100'}
    return {'last_score':'{:.3f}'.format(30.28475), 'figPath':'../'+figPath, 'movement':'100'}


@eel.expose
def save():
    global lmLog
    np.save(os.path.join(resultDir, np.array(lmLog)))
    return 1


eel.init("./")
eel.start("web/select.html", port=8000)