from maya import cmds
import random

# We import the baseWindow module which lets us reuse parts of the Window class
import baseWindow

# We create a new RandomizerUI class that inherits from baseWindow.Window
# This means we get all the behaviors of the Window class without redefining itself
class RandomizerUI(baseWindow.Window):

    # We can redefine parts of Window or add our own methods
    # if we redefine something, it's called overriding it
    def __init__(self, name='Randomizer'):
        # The super function lets us call our parent class
        # in this case it will call the window class, and then call its __init__ method
        # We use this to reuse functionality from the super or parentclass
        # even if we are overriding the method
        super(RandomizerUI, self).__init__(name)

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.frameLayout(label="Choose an object type")

        cmds.columnLayout()
        self.objType = cmds.radioCollection("objectCreationType")
        cmds.radioButton(label="Sphere")
        cmds.radioButton(label="Cube", select=True)
        cmds.radioButton(label="Cone")

        self.intField = cmds.intField("numObjects", value=3)

        cmds.setParent(column)
        frame = cmds.frameLayout("Choose your max ranges")

        cmds.gridLayout(numberOfColumns=2, cellWidth=100)

        for axis in 'xyz':
            cmds.text(label='%s axis' % axis)
            cmds.floatField('%sAxisField' % axis, value=random.uniform(0, 10))

        cmds.setParent(frame)
        cmds.rowLayout(numberOfColumns=2)

        cmds.radioCollection("randomMode")
        cmds.radioButton(label='Absolute', select=True)
        cmds.radioButton(label='Relative')

        cmds.setParent(column)
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(label="Create", command=self.onCreateClick)
        cmds.button(label="Randomize", command=self.onRandomClick)

    def onCreateClick(self, *args):
        radio = cmds.radioCollection(self.objType, query=True, select=True)
        mode = cmds.radioButton(radio, query=True, label=True)

        numObjects = cmds.intField(self.intField, query=True, value=True)

        createObjects(mode, numObjects)
        onRandomClick()

    def onRandomClick(self, *args):
        radio = cmds.radioCollection("randomMode", query=True, select=True)
        mode = cmds.radioButton(radio, query=True, label=True)

        for axis in 'xyz':
            val = cmds.floatField("%sAxisField" % axis, query=True, value=True)
            randomize(minValue=val*-1, maxValue=val, mode=mode, axes=axis)


def createObjects(mode, numObjects=5):
    """This creates objects. Supports Cubes, Spheres, Cylinder and Cones"""
    objList = []
    
    # create a number of objects of the given type
    for n in range(numObjects):
        if mode == 'Cube':
            obj = cmds.polyCube()
        elif mode == 'Sphere':
            obj = cmds.polySphere()
        elif mode == "Cylinder":
            obj = cmds.polyCylinder()
        elif mode == 'Cone':
            obj = cmds.polyCone()
        else: cmds.error("I don't know what to create")
        
        objList.append(obj[0])
        
    cmds.select(objList)
    return objList

def randomize(objList=None, minValue=0, maxValue=10, axes='xyz', mode='Absolute'):
    if objList is None:
        objList = cmds.ls(selection=True)
        
    for obj in objList:
        for axis in axes:
            current = 0
            if mode == 'Relative':
                current = cmds.getAttr(obj+'.t%s' % axis)
            
            val = current + random.uniform(minValue, maxValue)
            cmds.setAttr(obj+'.t%s' % axis, val)

