from random import randint
from asciimatics.screen import Screen

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GraphicalRepresentation:
    def __init__(self, position, characterMatrix, color, background):
        self.position = position
        self.characterMatrix = characterMatrix
        self.color = color
        self.background = background

    def draw(self, screen):
        x = self.position.x
        y = self.position.y
        for column in self.characterMatrix:
            x = self.position.x
            for cell in column:
                screen.print_at(cell, x, y, self.color, self.background)
                x += 1
            y += 1
        

class EntityRepresentation:
    def __init__(self, graphicalRepresentation, entity):
        self.graphicalRepresentation = graphicalRepresentation
        self.entity = entity


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
            gr.draw(screen)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()
        

def test_graphical_representation(screen):
    testCharacterMatrix = [
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
    ]
    graphicalRepresentations = [GraphicalRepresentation(Point(0,0), testCharacterMatrix, Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)]
    draw_graphical_representations(graphicalRepresentations, screen)

if __name__ == "__main__":
    Screen.wrapper(test_graphical_representation)