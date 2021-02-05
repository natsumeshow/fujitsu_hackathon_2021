import eel
import random

@eel.expose #define function adding '@eel.expose'
def python_function():
    return "return from python_function"

list = [[600, 150], [550, 200], [500, 250], [450, 300], [650, 200], [700, 250], [750, 300], [575, 275], [550, 350], [525, 425], [625, 275], [650, 350], [675, 425], [600, 200]]

@eel.expose
def disp_score(time):
    score = random.randint(0,100)
    for i in range(13):
        for j in range(2):
            list[i][j] += random.randint(-3, 3)


    val = {"score": score, "landmark": list}
    return val

eel.init(".")
eel.start("web/select.html") #first page
