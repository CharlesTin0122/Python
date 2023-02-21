import pymel.core as pm


a = pm.selected()
t = a[0].getTranslation()
r = a[0].getRotation()
s = a[0].getScale()
att = a[0].listAnimatable()
dir(a[0])