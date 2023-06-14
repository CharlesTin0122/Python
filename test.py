import pymel.all as pm
pm.env.setUpAxis("z")
panel = str(pm.getPanel(withFocus=1))
pm.viewSet(
    pm.mel.hotkeyCurrentCamera(panel),
    animate=pm.optionVar(query='animateRoll'),
    home=1
    )
