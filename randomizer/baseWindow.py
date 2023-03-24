from maya import cmds

# A class is a description of an object and its behavior
# In this case we are describing how a window should behave
#
# Classes are defined like functions but they use the class keyword
# They also take a parameter to describe what they inherit from
# i.e. the Window object gets all the properties of Object
#
# We can create a window by calling the class with parenthesis
# win = Window('myWin')
#
# This is called creating an instance of the class
#
#

class Window(object):

    # Classes can also take parameters.
    # It takes parameters using the __init__ method
    # This method is called whenever you create a new instance of the class
    # In this case our Window class always requires a name to be given
    # The self paramter is always given automatically and it allows an instance to differentiate itself
    # i.e. if you have two windows, self makes sure they dont refer to each other accidentally.
    def __init__(self, name):
        
        # In our __init__ we call the same UI code to create a window
        # and to close existing ones if they exist
        if cmds.window(name, query=True, exists=True):
            cmds.deleteUI(name)

        cmds.window(name)
        # The self keyword lets a class refer to parts of itself
        # in this case it's refering to its own buildUI method
        # Methods are what functions are called when part of a class
        self.buildUI()
        cmds.showWindow()

    def buildUI(self):
        print("No UI is defined")