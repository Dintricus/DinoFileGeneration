from asciimatics.screen import Screen
from graphics import draw_square, CAMERA_POINT, GLOBAL_SLEEP_TIME
from entities import Point
import time



class CloneEntity:
	def __init__(self, clonePosition, windowPosition, windowSize):
		self.clonePosition = clonePosition
		self.windowPosition = windowPosition
		self.windowSize = windowSize
		self.active = True
		self.currentSelection = 0

	def drawScreen(self, screen, entities, components):
		titleLine = 1
		screen.print_at('Select your entity to clone (press "y" to select):', 1, titleLine, Screen.COLOUR_WHITE, Screen.COLOUR_BLUE)
		i = 0
		for entity in entities:
			if self.currentSelection == i:
				screen.print_at(str(i)+": "+str(entity), 1, titleLine+2+i, Screen.COLOUR_GREEN, Screen.COLOUR_BLUE)
			else:
				screen.print_at(str(i)+": "+str(entity), 1, titleLine+2+i, Screen.COLOUR_WHITE, Screen.COLOUR_BLUE)
			i += 1
		pass

	def kill(self, parent):
		parent.cloneEntity = None
		self.active = False

	def cloneEntity(self, position, entities, entity):
		newEntity = entity.clone()
		goc = newEntity.getComponent("GameObjectComponent")
		if goc is not None:
			goc.graphicalRepresentation.position = position.clone()
		entities.append(newEntity)
		pass

	def processInput(self, screen, entities, parent, components):
		ev = screen.get_key()
		if ev in (ord('W'), ord('w')):
			self.currentSelection = max(0, self.currentSelection - 1)
			return
		if ev in (ord('S'), ord('s')):
			self.currentSelection = min(len(entities), self.currentSelection + 1)
			return
		if ev in (ord('Y'), ord('y')):
			self.cloneEntity(self.clonePosition, entities, entities[self.currentSelection])
			self.kill(parent)
			return
		if ev in (ord('Q'), ord('q')):	# KILL ITSELF IF 'Q' IS PRESSED
			self.kill(parent)
			return
		pass

	def update(self, screen, entities, parent, components):
		while self.active:
			self.processInput(screen, entities, parent, components)
			self.drawScreen(screen, entities, components)
			screen.refresh()
			time.sleep(GLOBAL_SLEEP_TIME)
			screen.clear_buffer(fg=Screen.COLOUR_WHITE, attr=Screen.A_NORMAL, bg=Screen.COLOUR_BLUE)