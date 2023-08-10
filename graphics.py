from random import randint
from asciimatics.screen import Screen
import time
import sys
import logging

# CHARACTER MATRICES
ASCII_REPRESENTATIONS = {
    "NOTHING": [[]],
    "TEST": [
        ["/", "=", "=", "\\"],
        ["|", "T", "E", "|"],
        ["|", "S", "T", "|"],
        ["\\", "=", "=", "/"],
    ],
    "CURSOR": [
        [" ", " ", " ", " "],
        [" ", "/", "\\", " "],
        [" ", "\\", "/", " "],
        [" ", " ", " ", " "],
    ]
}

def getAsciiRepresentation(name):
    return ASCII_REPRESENTATIONS.get(name)


SCALE = 4 # 1 SQUARE = 4X4 MATRIX

# START OF TREE PRINT GLOBAL VARIABLES
SPACES_PER_TAB = 4
# END OF TREE PRINT GLOBAL VARIABLES

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "Point{x="+str(self.x)+", y="+str(self.y)+"}"

# START OF GRAPHICAL REPRESENTATION GLOBAL VARIABLES
GLOBAL_POINT = Point(0, 0)
CAMERA_POINT = Point(0, 0)
GLOBAL_BACKGROUND = Screen.COLOUR_BLACK
GLOBAL_FOREGROUND = Screen.COLOUR_WHITE
SCREEN_HEIGHT = 50
SCREEN_WIDTH = 50
# END OF GRAPHICAL REPRESENTATION GLOBAL VARIABLES

class GraphicalRepresentation:
    def __init__(self, position, characterMatrix, color, background):
        self.position = position
        self.characterMatrix = characterMatrix
        self.color = color
        self.background = background

    def draw(self, position, screen):
        x = (position.x + self.position.x) * SCALE
        y = (position.y + self.position.y) * SCALE
        for column in self.characterMatrix:
            x = (position.x + self.position.x) * SCALE
            for cell in column:
                screen.print_at(cell, x, y, self.color, self.background)
                x += 1
            y += 1
    
    def move(self, x, y):
        self.position.x += x
        self.position.y += y

    def __str__(self):
        return "GraphicalRepresentation{position="+str(self.position)+", characterMatrix="+str(self.characterMatrix)+", color="+str(self.color)+", background+"+str(self.background)+"}"

def ascii_hello_world(screen):
    while True:
        screen.print_at('Hello world!',
                        randint(0, screen.width), randint(0, screen.height),
                        colour=randint(0, screen.colours - 1),
                        bg=randint(0, screen.colours - 1))
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()


def draw_graphical_representations(graphicalRepresentations, screen):
    while True:
        for gr in graphicalRepresentations:
            gr.draw(Point(0, 0), screen)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()

def draw_node_representations(entityRepresentations, screen):
    while True:
        for er in entityRepresentations:
            er.graphicalRepresentation.draw(screen)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()  

def test_graphical_representation(screen):
    testCharacterMatrix = getAsciiRepresentation("TEST")
    graphicalRepresentations = [GraphicalRepresentation(Point(0,0), testCharacterMatrix, Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)]
    draw_graphical_representations(graphicalRepresentations, screen)

def drawNode(screen, node, depth, line):
    gr = GraphicalRepresentation(Point(SPACES_PER_TAB*depth, line), [[node.__str__()]], Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)
    gr.draw(Point(GLOBAL_POINT.x, GLOBAL_POINT.y), screen)
    print_nodes(screen, node.definitions, depth, line)
    print_nodes(screen, node.children, depth, line+len(node.definitions))

def print_nodes(screen, nodes, depth=0, line=0):
    for node in nodes:
        print(((depth*SPACES_PER_TAB)*" ")+str(node))
        #drawNode(screen, node, depth, line)
        line += 1
        print_nodes(screen, node.definitions, depth+1, line)
        line += len(node.definitions)
        print_nodes(screen, node.children, depth+1, line)
        line += node.getDepthChildrenLen()
    return line

def print_entities_test(screen, entities):
    for entity in entities:
        depth = 0
        print(((depth*SPACES_PER_TAB)*" ")+str(entity))
        depth = 1
        for component in entity.components:
            print(((depth*SPACES_PER_TAB)*" ")+str(component))


def logInformation(entities, screen):
    logging.debug("CAMERA_POINT="+str(CAMERA_POINT))

def draw_entities(entities, screen):
    screen.clear()
    print('\e[8;'+str(SCREEN_HEIGHT)+';'+str(SCREEN_WIDTH)+'t')
    while True:
        for entity in entities:
            #logging.debug("Drawing "+str(entity)+".")
            entity.draw(screen, Point(CAMERA_POINT.x, CAMERA_POINT.y), entities, entity, entity.components)
        time.sleep(0.01)
        screen.refresh()
        screen.clear_buffer(fg=GLOBAL_FOREGROUND, attr=Screen.A_NORMAL, bg=GLOBAL_BACKGROUND)
        logInformation(entities, screen)

if __name__ == "__main__":
    Screen.wrapper(test_graphical_representation)