import xml.etree.ElementTree as ET
from xml.dom import minidom
import xml.dom.minidom
from asciimatics.screen import Screen
from graphics import print_nodes
import logging

TEST_FILE_PATH = "files/test_world.xml"

ENTITY_METANAME = ["entity", "ent"]
MAP_MAKER_COMPONENT = ["mapMakerComponent", "mmc"]
COMPONENT_METANAME = ["component", "comp"] + MAP_MAKER_COMPONENT
FACTORY_METANAME = ["factory", "fact"]
DEFINITION_METANAME = ["definition", "def"]

logger = logging.getLogger(__name__)

class Definition:
    def __init__(self, metaName, name, description, format, value):
        self.metaName = metaName
        self.name = name
        self.description = description
        self.format = format
        self.value = value
        self.children = []
        self.definitions = []
        logger.debug(self.__str__()+" created.")

    def __str__(self):
        return "Definition{metaName="+self.metaName+", name="+self.name+", description="+self.description+", format="+self.format+", value="+self.value+"}"

    def isMatch(self, def1):
        return self.name == def1.name and self.format == def1.format

    def getDepthChildrenLen(self):
        result = len(self.children)
        for child in self.children:
            result += child.getDepthChildrenLen()
        return result
    
    def clone(self):
        clonedChildren = []
        clonedDefinitions = []
        for child in self.children:
            clonedChildren.append(child.clone())
        for child in self.definitions:
            clonedDefinitions.append(child.clone())
        result = Definition(self.metaName, self.name, self.description, self.format, self.value)
        result.children = clonedChildren
        result.definitions = clonedDefinitions
        return result
    
    def toXML(self, root, parent):
        result = ET.SubElement(parent, self.metaName)
        result.set('name', self.name)
        result.set('description', self.description)
        result.set('format', self.format)
        result.set('value', self.value)
        return result

class Node:
    def __init__(self, metaDefinition, definitions, children):
        self.metaDefinition = metaDefinition
        self.definitions = definitions
        self.children = children
        logger.debug(self.__str__()+" created.")

    def __str__(self):
        return "Node{metaDefinition="+self.metaDefinition.__str__()+", definitions.amount="+str(len(self.definitions))+", children.amount="+str(len(self.children))+"}"
    
    def getDepthChildrenLen(self):
        result = len(self.children)
        for child in self.children:
            result += child.getDepthChildrenLen()
        return result
    
    def getDefinition(self, name):
        for definition in self.definitions:
            if definition.name == name:
                return definition
        return None

    def isValid(self, factory):
        for factoryDef in factory.definitions:
            definition = self.getDefinition(factoryDef.name)
            if definition is None or not factoryDef.isMatch(definition): return False
        return True
    
    def toXML(self, root, parent):
        result = ET.SubElement(parent, self.metaDefinition.metaName)
        result.set('name', self.metaDefinition.name)
        result.set('description', self.metaDefinition.description)
        result.set('format', self.metaDefinition.format)
        result.set('value', self.metaDefinition.value)
        for definition in self.definitions: definition.toXML(root, result)
        for child in self.children: child.toXML(root, result)
        return result

def readXML(filepath):
    result = ET.parse(filepath)
    return result

def writeXML(filepath, root):
    root.write(filepath)
        

def writeNodesToXML(filepath, nodes):
    root = minidom.Document()
    root = ET.Element("xml")
    for node in nodes:
        node.toXML(root, root)
    writeXML(filepath, ET.ElementTree(root))

def createDefinitionFromXML(currentXMLNode):
    return Definition(
            currentXMLNode.tag,
            currentXMLNode.attrib['name'],
            currentXMLNode.attrib['description'],
            currentXMLNode.attrib['format'],
            currentXMLNode.attrib['value'],
        )

def depthFirstXMLGeneration(document, currentXMLNode=None):
    #get tag: node.tag
    # get attribute list: node.attrib
    result = None
    if currentXMLNode is None:      # IS ROOT
        result = []
        for child in document:
            result.append(depthFirstXMLGeneration(document, child))
    
    elif DEFINITION_METANAME.__contains__(currentXMLNode.tag):  # IS DEFINITION
        result = createDefinitionFromXML(currentXMLNode)
    
    else:   # IS NODE
        metaDefinition = createDefinitionFromXML(currentXMLNode)
        definitions = []
        children = []
        for child in currentXMLNode:
            childNode = depthFirstXMLGeneration(document, child)
            if DEFINITION_METANAME.__contains__(child.tag):
                definitions.append(childNode)
            else:
                children.append(childNode)
        result = Node(metaDefinition, definitions, children)
    return result

def generateFromXML(filepath):
    root = readXML(filepath).getroot()
    return depthFirstXMLGeneration(root)


def test_file_generation(screen):
    logger.setLevel(logging.DEBUG)
    logger.debug("Starting test file generation.")
    nodes = generateFromXML(TEST_FILE_PATH)
    logger.debug("File "+TEST_FILE_PATH+" generated successfully.")
    '''
    while True:
        print_nodes(screen, nodes)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()
        time.sleep(0.1)
    '''
    print_nodes(screen, nodes)
    logger.debug("Writing generated elements to same test file.")
    writeNodesToXML(TEST_FILE_PATH, nodes)
    logger.debug("Finished writting to test file.")


if __name__ == "__main__":
    Screen.wrapper(test_file_generation)