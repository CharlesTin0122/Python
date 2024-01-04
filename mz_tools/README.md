# From https://mayazoo.net/index.html
# Install
Place mzSnakeTool.py in your Maya scripts folder.
(Usually found in the following folders.)

    Windows:
    \Users\<username>\Documents\maya\scripts
    Mac OS:
    /Users/<username>/Library/Preferences/Autodesk/maya/scripts
    Linux:
    /home/<username>/maya/scripts

Run the script using a python command
Open the Maya Script Editor. ( Windows > General Editors > Script Editor)
Click on a Python tab and type in the following lines of code:


    import mzSnakeTool as mst
    mst.mzSnakeTool_UI()


    import mzFishTool as mft
    mft.mzFishTool_UI()


    import mzButterflyTool as mbt
    mbt.mzButterflyTool_UI()


    import mzControlTool as mct
    mct.mzControlTool()



