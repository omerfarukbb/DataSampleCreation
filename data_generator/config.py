import os

BG_WIDTH = 4000
BG_HEIGHT = 3000
COLOR_NOISE = 30
ODLC_WIDTH_RANGE = (540, 541)
ODLC_ROTATE_RANGE = (-5, 5)
ODLC_COUNT_PROBS = {
    0 : 0.25, 
    1 : 0.75, 
    2 : 0.0, 
    3 : 0.0
}

SCRIPT_DIR = os.getcwd()
BACKGROUNDS = os.listdir(os.path.join(SCRIPT_DIR, "background"))

SHAPES = ["circle", "cross", "heptagon", "hexagon", "octagon", "pentagon", 
"quartercircle", "rect", "semicircle", "square", "star", "trapezoid", "triangle"]
ALPHANUMERICS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
                "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",  
                "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

COLORS_DICT = {
    "red" : (0, 0, 255), 
    "green" : (0, 255, 0), 
    "blue": (219, 152, 52),
    "yellow" : (0,255,255),
    "orange" : (0,165,255), 
    "purple" : (128,0,128),
    "brown" : (63,133,205),
    "gray" : (19,69,139),
    "black" : (0,0,0),
    "white" : (255,255,255)
}

COLORS_DICT_HSV = {
    'red': [[189, 255, 255], [159, 50, 70]], 
    #'red2': [[9, 255, 255], [0, 50, 70]], 
    'green': [[89, 255, 255], [36, 50, 70]], 
    'blue': [[128, 255, 255], [90, 50, 70]], 
    'yellow': [[35, 255, 255], [25, 50, 70]], 
    'orange': [[24, 255, 255], [10, 50, 70]], 
    'purple': [[158, 255, 255], [129, 50, 70]],
    'brown': [[20, 255, 200], [10, 100, 20]],
    'gray': [[180, 18, 230], [0, 0, 40]],
    'black': [[180, 255, 30], [0, 0, 0]], 
    'white': [[180, 18, 255], [0, 0, 231]],   
}

COLOR_NAMES = list(COLORS_DICT.keys())
COLORS = list(COLORS_DICT.values())
COLORS_HSV = list(COLORS_DICT_HSV.values())

SAVE_SHAPE_LABEL = True
SAVE_ALPHA_LABEL = False