import eel

@eel.expose #define function adding '@eel.expose'
def python_function():
    return "return from python_function"

eel.init("web")
eel.start("select.html") #first page