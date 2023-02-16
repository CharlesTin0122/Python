import pymel.core as pm

def smoothAnimCurve():

	AnimCurve = pm.keyframe(q=True,n=True)
	for cv in AnimCurve:

		keys = pm.keyframe(cv,q=True,sl=True)
		sizeOfKeys = len(keys)

		if (sizeOfKeys < 3):
			continue

		dupCurve = pm.duplicate(cv)

		for i in range(1,sizeOfKeys-1):
			preVal = pm.keyframe(cv,time=(keys[i-1],keys[i-1]),q=True,vc=True)
			curVal = pm.keyframe(cv,time=(keys[i],keys[i]),q=True,vc=True)
			nexVal = pm.keyframe(cv,time=(keys[i+1],keys[i+1]),q=True,vc=True)
			aveVal = (preVal[0] + curVal[0] + nexVal[0]) / 3
			pm.keyframe(dupCurve,time=(keys[i],keys[i]),a=True,vc=aveVal)

		for i in range(1,sizeOfKeys-1):
			dupCurVal = pm.keyframe(dupCurve,time=(keys[i],keys[i]),q=True,vc=True)
			pm.keyframe(cv,time=(keys[i],keys[i]) ,a=1 ,vc=dupCurVal[0])

		pm.delete(dupCurve[0])