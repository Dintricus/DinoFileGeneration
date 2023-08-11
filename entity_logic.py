from asciimatics.screen import Screen
from graphics import draw_square, CAMERA_POINT, GLOBAL_SLEEP_TIME, Window
from entities import Point
from file_processing import writeNodesToXML, FILE_DIR_PATH
import logging
import time



class CloneEntity(Window):
	def __init__(self, clonePosition):
		super().__init__("Select your entity to clone (press 'Y' to select):")
		self.clonePosition = clonePosition
		self.active = True
		self.currentSelection = 0

	def cloneEntity(self, position, entities, entity):
		newEntity = entity.clone()
		goc = newEntity.getComponent("GameObjectComponent")
		if goc is not None:
			newEntity.getComponent("GameObjectComponent").graphicalRepresentation.position = position.clone()
		entities.append(newEntity)
		pass

	def performAction(self, options, option, parentGameEntity):
		self.cloneEntity(self.clonePosition, options, option)
		self.kill(parentGameEntity)

def saveFile(entities):
	logging.debug("Start saving file.")
	filepath = None
	for entity in entities:
		if entity.definition.format == "WorldFileEntity":
			filepath = entity.definition.value
			nodes = []
			for entity in entities:
				nodes.append(entity.toNode())
			logging.debug("World saved to file "+str(filepath+"."))
			return writeNodesToXML(FILE_DIR_PATH+"/"+filepath, nodes)
	return None