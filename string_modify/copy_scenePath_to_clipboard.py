import maya.cmds as cmds
import subprocess
import sys

# Get current scene-name
sceneName = cmds.file(sceneName=True, query=True)

try:
    if sys.platform == "darwin":
        process = subprocess.Popen(
            "pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE
        )
        process.communicate(sceneName.encode("utf-8"))
    elif sys.platform == "linux2":
        print("Copy log on linux are currently not supported")
    elif sys.platform is "windows" or "win32" or "win64":
        # Copy to clipboard
        clipboard = cosmos.qtCore.QtWidgets.QApplication.clipboard()
        clipboard.setText(sceneName)
    # Show success
    cosmos.displayViewMessage("Log copied to clipboard", "good")
except Exception as message:
    print(message)
    cosmos.displayViewMessage(
        "Problem copy the clipboard data. Try ':sendLog'", "error"
    )
