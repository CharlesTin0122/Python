# Import our libraries
from maya import cmds
# The partial command lets us store a function with a variable to call later
# This lets us tell many buttons to call the same function but with different variables
from functools import partial

def align(nodes=None, axis='x', mode='mid'):
    # default nodes to selection if nothings provided
    if not nodes:
        nodes = cmds.ls(sl=True)

    # If nothing is selected either, then error
    if not nodes:
        cmds.error('Nothing selected or provided')

    # We need to convert any vertexes, edges and faces to just vertexes and flatten any ranges
    # If we don't flatten we might get polyCube1.vtx[1:5] which is hard to work with
    # We instead just want polyCube1.vtx[1], polyCube1.vtx[2], polyCube1.vtx[3] etc...

    # Create a temporary list to store the converted objects in
    _nodes = []
    for node in nodes:
        # Faces are in the format polyCube1.f[2]
        # So we check if its a face by looking for .f[ inside the name
        if '.f[' in node:
            # If its a face, we convert it from a face to a vertex list
            node = cmds.polyListComponentConversion(node, fromFace=True, toVertex=True)
        elif '.e[' in node:
            # We do the same for edges
            node = cmds.polyListComponentConversion(node, fromEdge=True, toVertex=True)

        # To flatten the vertex lists we need to first select it
        cmds.select(node)
        # Then we can use the ls command to flatten it out
        node = cmds.ls(sl=True, fl=True)

        # Then we extend the _nodes list with this flat list
        _nodes.extend(node)

    # Since we changed the selection, lets set it back to the nodes list
    cmds.select(nodes)
    # Then lets replace nodes with the _nodes temp list that we made
    nodes = _nodes

    # Now we need to figure out which mode we're using
    # We do this by seeing if mode is equal to a value which gives us True or Fale
    # We then store that True or False in a variable
    minMode = mode == 'min'
    maxMode = mode == 'max'
    midMode = mode == 'mid'

    # All our transform values give us back a list of x,y,z
    # Since we only care about one of these axes at a time, 
    # the start variable tells us where to look
    # For x we look at the first item (0), y is second (1) and z is third (2)
    # Remember that lists start from 0
    if axis == 'x':
        start = 0
    elif axis == 'y':
        start = 1
    elif axis == 'z':
        start = 2
    else:
        # If none of these apply then error out
        cmds.error('Unknown Axis')

    # We need to store the values and bounding boxes
    bboxes = {}    
    values = []

    # get the dimensions of our objects by looping through them
    for node in nodes:
        if '.vtx[' in node:
            # Vertexes dont have bounding boxes so we just get their worldspace translation values
            ws = cmds.xform(node, q=True, t=True, ws=True)
            # In this case minValue, midValue and maxValue will all be equal so we can assign them together
            minValue = midValue = maxValue = ws[start]
        else:
            # If we are a regular object, then get the bounding box of the object
            # this is a box that describes the height, width and depth of an object
            # It gives us back a list like
            # [x-min, y-min, z-min, x-max, y-max, z-max]
            bbox = cmds.exactWorldBoundingBox(node)

            # Then we get the minimum value, the max value and use them to calculate the mid value
            minValue = bbox[start]
            maxValue = bbox[start+3]
            midValue = (maxValue+minValue)/2

        # We store these in the bboxes dictionary using the node name as the key
        bboxes[node] = (minValue, midValue, maxValue)

        # Depending on the mode, we only store that modes value for later use
        if minMode:
            values.append(minValue)
        elif maxMode:
            values.append(maxValue)
        else:
            values.append(midValue)

    # we calculate the alignment point using the values collected
    if minMode:
        # This gives us back the minimum values. min is a python built in function
        target=min(values)
    elif maxMode:
        # This gives us back the maximum values. max is a python built in function        
        target = max(values)
    else:
        # This is a formula to average the values
        target = sum(values)/len(values)

    # figure out the distance to the target
    for node in nodes:
        # Retrieve the values from the dictionary
        bbox = bboxes[node]
        # Extract them into variables
        minValue, midValue, maxValue = bbox

        # then get the worldspace transform
        ws = cmds.xform(node, query=True,
                        translation=True,
                        ws=True)

        # Finally use those values to calculate how far to move the objects
        width = maxValue - minValue
        if minMode:
            distance = minValue - target
            ws[start] = (minValue-distance) + width/2
        elif maxMode:
            distance = target-maxValue
            ws[start] = (maxValue + distance) - width/2
        else:
            distance = target - midValue
            ws[start] = midValue + distance

        # move the object to the target
        cmds.xform(node, translation=ws, ws=True)

class Aligner(object):
    """_summary_

    Args:
        object (_type_): _description_
    """

    def __init__(self):
        # Create the window and make sure only one exists at a time
        name = "Aligner"
        if cmds.window(name, query=True, exists=True):
            cmds.deleteUI(name)
        
        window = cmds.window(name)
        self.buildUI()
        cmds.showWindow()
        cmds.window(window, e=True, resizeToFitChildren=True)

    def buildUI(self):
        column = cmds.columnLayout()
        # Add radio buttons for axis
        cmds.frameLayout(label="Choose an axis")

        cmds.gridLayout(numberOfColumns=3, cellWidth=50)
        
        cmds.radioCollection()
        self.xAxis = cmds.radioButton(label='x', select=True)
        self.yAxis = cmds.radioButton(label='y')
        self.zAxis = cmds.radioButton(label='z')

        # Create the icon button using the given icon
        # the partial command tells the button to call the onOptionClick method
        # and it also tells it to use the xAxis variable in this case
        createIconButton('XAxis.png', command=partial(self.onOptionClick, self.xAxis))
        createIconButton('YAxis.png', command=partial(self.onOptionClick, self.yAxis))
        createIconButton('ZAxis.png', command=partial(self.onOptionClick, self.zAxis))

        # Add radio buttons for mode
        cmds.setParent(column)

        cmds.frameLayout(label="Choose where to align")

        cmds.gridLayout(numberOfColumns=3, cellWidth=50)
        
        cmds.radioCollection()
        self.minMode = cmds.radioButton(label='min')
        self.midMode = cmds.radioButton(label='mid', select=True)
        self.maxMode = cmds.radioButton(label='max')

        createIconButton('MinAxis.png', command=partial(self.onOptionClick, self.minMode))
        createIconButton('MidAxis.png', command=partial(self.onOptionClick, self.midMode))
        createIconButton('MaxAxis.png', command=partial(self.onOptionClick, self.maxMode))
        

        # add apply button
        cmds.setParent(column)
        # BGC gives the button a background color. In this case, it's blue
        # Values are R,G,B
        cmds.button(label='Align', command=self.onApplyClick, bgc=(0.2, 0.5, 0.9))

    def onOptionClick(self, opt):
        # This function will receive a variable from the buttons
        # this variable is the name of the radio button
        # and it will tell it to be selected
        cmds.radioButton(opt, edit=True, select=True)

    def onApplyClick(self, *args):
        # get the axis
        if cmds.radioButton(self.xAxis, q=True, select=True):
            axis = 'x'
        elif cmds.radioButton(self.yAxis, q=True, select=True):
            axis = 'y'
        else:
            axis = 'z'

        # get the mode
        if cmds.radioButton(self.minMode, q=True, select=True):
            mode = 'min'
        elif cmds.radioButton(self.midMode, q=True, select=True):
            mode = 'mid'
        else:
            mode = 'max'

        # call the align function
        align(axis=axis, mode=mode)

def getIcon(icon):
    import os
    # This script is in the scripts directory
    # __file__ is the full path to this script file
    # os.path.dirname gives us back the directory name where this file is stored
    scripts = os.path.dirname(__file__)

    # os.path.join joints the paths together 
    icons = os.path.join(scripts, 'icons')

    # finally we find the icon and return its full path
    icon = os.path.join(icons, icon)
    return icon

def createIconButton(icon, command=None):
    if command:
        cmds.iconTextButton(image1=getIcon(icon), width=50, height=50, command=command)
    else:
        cmds.iconTextButton(image1=getIcon(icon), width=50, height=50)
                