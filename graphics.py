from random import randint
from asciimatics.screen import Screen
import time
import sys
import math
import logging

# CHARACTER MATRICES
EMPTY_STRING = [""]

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
	
	def asTurtle(self):
		return (self.x, self.y)
	
	def clone(self):
		return Point(self.x, self.y)

# START OF GRAPHICAL REPRESENTATION GLOBAL VARIABLES
#GLOBAL_POINT = Point(round(sys.maxsize/2), round(sys.maxsize/2))
GLOBAL_POINT = Point(0, 0)
CAMERA_POINT = Point(0, 0)    # TOP LEFT CORNER OF THE WINDOW
GLOBAL_BACKGROUND = Screen.COLOUR_BLACK
GLOBAL_FOREGROUND = Screen.COLOUR_WHITE
SCREEN_HEIGHT = 50
SCREEN_WIDTH = 50
GLOBAL_SLEEP_TIME = 0.05
# END OF GRAPHICAL REPRESENTATION GLOBAL VARIABLES

class GraphicalRepresentation:
	def __init__(self, position, characterMatrix, color, background):
		self.position = position
		self.characterMatrix = characterMatrix
		self.color = color
		self.background = background

	def draw(self, position, screen):
		# position = current camera
		# self.position = global position
		globalPosition = self.position
		y = (globalPosition.y + position.y) * SCALE
		for column in self.characterMatrix:
			x = (globalPosition.x + position.x) * SCALE
			for cell in column:
				if not EMPTY_STRING.__contains__(cell):
					screen.print_at(cell, x, y, self.color, self.background)
				x += 1
			y += 1
	

	def move(self, x, y):
		self.position.x += x
		self.position.y += y

	def __str__(self):
		return "GraphicalRepresentation{position="+str(self.position)+", characterMatrix="+str(self.characterMatrix)+", color="+str(self.color)+", background+"+str(self.background)+"}"

class Window:
	def __init__(self, title):
		self.title = title
		self.active = True
		self.currentOption = 0
	
	def drawScreen(self, screen, options):
		titleLine = 1
		screen.print_at(self.title, 1, titleLine, Screen.COLOUR_WHITE, Screen.COLOUR_BLUE)
		i = 0
		for entity in options:
			if self.currentSelection == i:
				screen.print_at(str(i)+": "+str(entity), 1, titleLine+2+i, Screen.COLOUR_GREEN, Screen.COLOUR_BLUE)
			else:
				screen.print_at(str(i)+": "+str(entity), 1, titleLine+2+i, Screen.COLOUR_WHITE, Screen.COLOUR_BLUE)
			i += 1

	def kill(self, parentGameEntity):
		parentGameEntity.cloneEntity = None
		self.active = False

	def performAction(self, options, option, parentGameEntity):
		#TODO OVERRIDE WITH SUBCLASSES
		pass


	def processInput(self, screen, options, parentGameEntity):
		ev = screen.get_key()
		if ev in (ord('W'), ord('w')):
			self.currentSelection = max(0, self.currentSelection - 1)
			return
		if ev in (ord('S'), ord('s')):
			self.currentSelection = min(len(options), self.currentSelection + 1)
			return
		if ev in (ord('Y'), ord('y')):
			self.performAction(options, options[self.currentSelection], parentGameEntity)
			return
		if ev in (ord('Q'), ord('q')):	# KILL ITSELF IF 'Q' IS PRESSED
			self.kill(parentGameEntity)
			return
		pass

	def update(self, screen, entities, parent, components):
		while self.active:
			self.processInput(screen, entities, parent)
			self.drawScreen(screen, entities)
			screen.refresh()
			time.sleep(GLOBAL_SLEEP_TIME)
			screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLUE)

def draw_square(screen, relativeTo, windowPosition, windowSize, color, background):
		globalPosition = windowPosition
		y = (globalPosition.y + windowPosition.y) * SCALE
		for column in range(0, windowSize.y):
			x = (globalPosition.x + windowPosition.x) * SCALE
			for cell in range(0, windowSize.x):
				if not EMPTY_STRING.__contains__(cell):
					screen.print_at(" ", x, y, color, background)
				x += 1
			y += 1


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
	pass

def draw_entities(entities, screen):
	screen.clear()
	print('\e[8;'+str(SCREEN_HEIGHT)+';'+str(SCREEN_WIDTH)+'t')
	while True:
		for entity in entities:
			#logging.debug("Drawing "+str(entity)+".")
			entity.draw(screen, Point(CAMERA_POINT.x, CAMERA_POINT.y), entities, entity, entity.components)
		time.sleep(GLOBAL_SLEEP_TIME)
		screen.refresh()
		screen.clear_buffer(fg=GLOBAL_FOREGROUND, attr=Screen.A_NORMAL, bg=GLOBAL_BACKGROUND)
		logInformation(entities, screen)

if __name__ == "__main__":
	Screen.wrapper(test_graphical_representation)