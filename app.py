import eel
import os
import numpy as np
from matplotlib import pyplot as plt
import uuid

id = 'unknown'
videoPath = ''
isValid = False
landmark = np.array([])
k = 0.00001
scoreLog = []
yLog = []
resultDir = 'unknown'

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
    global landmark, scoreLog, yLog
    # y = model(frame)
    y = np.random.randn(18,2)
    lm = landmark[:,t]
    s = score(y,lm)
    yLog.append(y)
    scoreLog.append(s)
    return '{:.3f}'.format(s)

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
    return {'last_score':'{:.3f}'.format(np.mean(scoreLog)), 'figPath':figPath, 'movement':'100'


@eel.expose
def save():
    np.save(os.path.join(resultDir, np.array(yLog)))
    return 1


eel.init("web")
eel.start("select.html", port=8000)