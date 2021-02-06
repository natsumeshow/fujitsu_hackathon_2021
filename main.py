import eel
import random

@eel.expose #define function adding '@eel.expose'
def python_function():
    return "return from python_function"

list = [[600, 150], [550, 200], [500, 250], [450, 300], [650, 200], [700, 250], [750, 300], [575, 275], [550, 350], [525, 425], [625, 275], [650, 350], [675, 425], [600, 200]]

@eel.expose
def select_dance(id):
    return "../data/0000.mp4"

@eel.expose
def disp_score(t):
    if t == -1:
        val = {"isPlaying": False}
        return val
    if t == -2:
        val = {"isPlaying": False}
        return val
    score = random.randint(0,100)
    for i in range(13):
        for j in range(2):
            list[i][j] += random.randint(-3, 3)


    val = {"isPlaying": True, "score": score, "landmark": list}
    return val

@eel.expose
def result():
    val = {"last_score": 82.1, "figPath": "./images/thumbnail_1.png", "movement": 8888}
    return val


eel.init(".")
eel.start("web/select.html") #first page
