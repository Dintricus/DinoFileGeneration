import math
from graphics import Point, print_entities_test,GraphicalRepresentation, draw_entities, GLOBAL_POINT, CAMERA_POINT, SCALE
from ascii_graphics import getAsciiRepresentation
from entity_logic import *
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

    def clone(self):
        clonedProperties = []
        for property in self.properties:
            clonedProperties.append(property.clone())
        result = Component(self.definition.clone(), clonedProperties)
        return result
    
    def toNode(self):
        return Node(self.definition, self.properties, [])

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
        self.cloneEntity = None

    def update(self, screen, position, entities, parentEntity, components):
        # MAIN LOGIC COMPONENT
        # Here is where you implement what each component does.
        if self.definition.format == "MapMakerInputComponent":
            # UPDATE CURSOR POSITION
            screenCenter = self.getScreenCenter(screen)
            for component in components:
                if component.isDrawableComponent:
                    component.graphicalRepresentation.position = screenCenter
                    #component.graphicalRepresentation.position = Point(2, 2)
            
            # UPDATE CLONE WINDOW
            if self.cloneEntity is not None:
                self.cloneEntity.update(screen, entities, self, components)
            else:
                # INTERPRET INPUT
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
                if ev in (ord('C'), ord('c')):
                    self.cloneEntity = CloneEntity(screenCenter)
                if ev in (ord('G'), ord('G')):
                    saveFile(entities)
                if ev in (ord('Q'), ord('q')):
                    screen.close()
                    exit()
        elif self.definition.format == "AsciiMapInformationComponent":
            # print debug information
            screen.print_at("GLOBAL="+str(GLOBAL_POINT), 0, 1, Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)
            screen.print_at("CAMERA="+str(CAMERA_POINT), 0, 2, Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)
            screen.print_at("CENTER="+str(self.getScreenCenter(screen)), 0, 3, Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)
            drawnPoint = Point(math.floor(screen.width / SCALE), math.floor(screen.height / SCALE))
            screen.print_at("RATIO="+str(screen.height / screen.width), 0, 4, Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)
            screen.print_at("ENTITIES="+str(len(entities)), 0, 5, Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)
            screen.print_at("TILE LENGTH="+str(drawnPoint), 0, 6, Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)

            # print selected component
            screenCenter = self.getScreenCenter(screen)
            entityInPosition = self.getEntityInPosition(entities, screenCenter)
            if entityInPosition is not None and entityInPosition.getComponent("MapMakerInputComponent") is None:
                screen.print_at(""+str(entityInPosition.definition.name), 0, screen.height-1, Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)
            else:
                screen.print_at("empty", 0, screen.height-1, Screen.COLOUR_WHITE, Screen.COLOUR_BLACK)

    def getScreenCenter(self, screen):
            screenCenterX = round(screen.width / ((2) * SCALE)) - CAMERA_POINT.x - 1
            screenCenterY = round(screen.height / ((2) * SCALE)) - CAMERA_POINT.y - 1
            trueScreenCenter = Point(screenCenterX, screenCenterY)
            return trueScreenCenter
    
    def getProperty(self, name):
        for property in self.properties:
            if property.name == name:
                return property
        return None

    def getEntityInPosition(self, entities, position):
        for entity in entities:
            gameObjectComponent = entity.getComponentByFormat("GameObjectComponent")
            if gameObjectComponent is not None:
                gocPosition = vector3ToPoint(gameObjectComponent.getProperty("position").value)
                if gocPosition.x == position.x and gocPosition.y == position.y:
                    return entity
        return None

    def __str__(self):
        result = "Component{type="+self.definition.format+", properties.amount="+str(len(self.properties))+", isDrawableComponent="+str(self.isDrawableComponent)
        if self.isDrawableComponent:
            result += ", graphicalRepresentation="+str(self.graphicalRepresentation)
        return result+"}"
    
    def draw(self, screen, position, entities, parentEntity, components):
        if self.isDrawableComponent:
            self.graphicalRepresentation.draw(position, screen)
        self.update(screen, position, entities, parentEntity, components)
    

class Entity:
    def __init__(self, definition, components):
        self.definition = definition
        self.components = components
    
    def __str__(self):
        return "Entity{definition="+str(self.definition)+", components.amount="+str(len(self.components))+"}"
    
    def toNode(self):
        nodeComponents = []
        for component in self.components:
            nodeComponents.append(component.toNode())
        return Node(self.definition, [], nodeComponents)

    def draw(self, screen, position, entities, parentEntity, components):
        for component in self.components:
            component.draw(screen, position, entities, parentEntity, components)
        
    def getComponent(self, name):
        for component in self.components:
            if component.definition.name == name:
                return component
        return None
            
    def getComponentByFormat(self, name):
        for component in self.components:
            if component.definition.format == name:
                return component
        return None
    
    def clone(self):
        clonedComponents = []
        for component in self.components:
            clonedComponents.append(component.clone())
        result = Entity(self.definition.clone(), clonedComponents)
        return result
    

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
    logging.debug("GENERATED ENTITIES: ")
    print_entities_test(screen, entities)
    draw_entities(entities, screen)

if __name__ == "__main__":
    Screen.wrapper(test_element_generation)