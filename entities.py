import math
from graphics import Point, getAsciiRepresentation, print_entities_test,GraphicalRepresentation, draw_entities, CAMERA_POINT, SCALE
from asciimatics.screen import Screen
from file_processing import *
import logging

DRAWABLE_COMPONENTS = ["GameObjectComponent"]

def vector3ToPoint(vector3):
    vector3.replace(" ", "")
    vector3 = vector3.split(",")
    return Point(math.floor(float(vector3[0])), math.floor(float(vector3[1])))

class Component:
    def __init__(self, definition, properties):
        self.definition = definition
        self.properties = properties
        self.isDrawableComponent = DRAWABLE_COMPONENTS.__contains__(self.definition.format)
        self.initializeGraphicalRepresentationIfDrawable()
        self.start()

    def initializeGraphicalRepresentationIfDrawable(self):
        if self.isDrawableComponent:
            graphicalRepresentation = GraphicalRepresentation(
                vector3ToPoint(self.getProperty("position").value),
                getAsciiRepresentation(self.getProperty("asciiRepresentation").value),
                Screen.COLOUR_WHITE,
                Screen.COLOUR_BLACK,
            )
            self.graphicalRepresentation = graphicalRepresentation

    def start(self):
        # MAIN LOGIC COMPONENT
        # Here is where you implement what each component does.
        pass

    def update(self, screen, entities, parentEntity, components):
        # MAIN LOGIC COMPONENT
        # Here is where you implement what each component does.
        if self.definition.format == "MapMakerInputComponent":
            screenCenterX = round(screen.height / (2*SCALE)) + 1
            screenCenterY = round(screen.height / (4*SCALE)) + 1
            screenCenter = Point(screenCenterX, screenCenterY)
            logging.debug("screenCenter="+str(screenCenter))
            for component in components:
                if component.isDrawableComponent:
                    component.graphicalRepresentation.position = screenCenter
            
            ev = screen.get_key()
            if ev in (ord('W'), ord('w')):
                CAMERA_POINT.y += int(self.getProperty("speed").value)
                return
            if ev in (ord('S'), ord('s')):
                CAMERA_POINT.y -= int(self.getProperty("speed").value)
                return
            if ev in (ord('A'), ord('a')):
                CAMERA_POINT.x += int(self.getProperty("speed").value)
                return
            if ev in (ord('D'), ord('d')):
                CAMERA_POINT.x -= int(self.getProperty("speed").value)
                return
            if ev in (ord('Q'), ord('q')):
                screen.close()
                exit()

    def getProperty(self, name):
        for property in self.properties:
            if property.name == name:
                return property
        return None

    def __str__(self):
        result = "Component{type="+self.definition.format+", properties.amount="+str(len(self.properties))+", isDrawableComponent="+str(self.isDrawableComponent)
        if self.isDrawableComponent:
            result += ", graphicalRepresentation="+str(self.graphicalRepresentation)
        return result+"}"
    
    def draw(self, screen, position, entities, parentEntity, components):
        if self.isDrawableComponent:
            if self.definition.format == "MapMakerInputComponent":
                relativePoint = Point(CAMERA_POINT.x+self.graphicalRepresentation.position.x, CAMERA_POINT.y+self.graphicalRepresentation.position.y)
            else:
                relativePoint = Point(position.x+self.graphicalRepresentation.position.x, position.y+self.graphicalRepresentation.position.y)
            self.graphicalRepresentation.draw(relativePoint, screen)
        else:
            self.update(screen, entities, parentEntity, components)
    

class Entity:
    def __init__(self, definition, components):
        self.definition = definition
        self.components = components
    
    def __str__(self):
        return "Entity{definition="+str(self.definition)+", components.amount="+str(len(self.components))+"}"
    
    def draw(self, screen, position, entities, parentEntity, components):
        for component in self.components:
            component.draw(screen, position, entities, parentEntity, components)
        
    def getComponent(self, name):
        for component in self.components:
            if component.definition.name == name:
                return component
        return None


def getFactoryFromEntityNode(factories, entityNode):
    for factory in factories:
        if factory.metaDefinition.value == entityNode.metaDefinition.format:
            return factory
    return None

def createElement(factories, node, factory=None, parent=None):
    logging.debug("createElement(node="+str(node)+")")
    if factory is None: factory = getFactoryFromEntityNode(factories, node)
    logging.debug("Using factory "+str(factory)+".")
    if not node.isValid(factory): return None

    elif ENTITY_METANAME.__contains__(node.metaDefinition.metaName):
        logging.debug("Is of entity type.")
        result = Entity(node.metaDefinition, [])
        for child in node.children:
            createElement(factories, child, factory=getFactoryFromEntityNode(factory.children, child),  parent=result)
    
    elif COMPONENT_METANAME.__contains__(node.metaDefinition.metaName):
        logging.debug("Is of component type.")
        result = Component(node.metaDefinition, node.definitions)
        parent.components.append(result)
    return result

def segregateElementsFromNodes(nodes):
    factories = []
    entityNodes = []
    for node in nodes:
        if FACTORY_METANAME.__contains__(node.metaDefinition.metaName):
            factories.append(node)
        elif ENTITY_METANAME.__contains__(node.metaDefinition.metaName):
            entityNodes.append(node)
    return factories, entityNodes

'''
    MAIN METHOD TO GENERATE ENTITIES AND COMPONENTS
'''
def generateEntitiesFromNodes(nodes):
    factories, entityNodes = segregateElementsFromNodes(nodes)
    result = []
    for en in entityNodes:
        result.append(createElement(factories, en))
    return result
    

'''
    TEST ENTITY AND COMPONENT GENERATION
'''
def test_element_generation(screen):
    logging.basicConfig(level=logging.DEBUG)
    nodes = generateFromXML(TEST_FILE_PATH)
    logging.info("\nGENERATED NODES:")
    print_nodes(screen, nodes)
    print("\n")
    entities = generateEntitiesFromNodes(nodes)
    logging.info("GENERATED ENTITIES: ")
    print_entities_test(screen, entities)
    draw_entities(entities, screen)

if __name__ == "__main__":
    Screen.wrapper(test_element_generation)