import pymel.core as pm

jntChain = []
clusterList = []
def creatJoint(jntCount,jntLength):
	global jntChain
	for i in range(jntCount):
		jnt = pm.joint(name='jnt_{}'.format(i+1),
								position=((i+1)*jntLength,0,0))
		jntChain.append(jnt)
	return  jntChain
	


def creatSplineIK(jntChain,numSpans):
	jntsplineIK = pm.ikHandle(sol='ikSplineSolver',name='tail_spline_IK',
												ns=numSpans,sj=jntChain[0],ee=jntChain[-1])
	jntsplineIK[2].rename('splineIK_curve')
	splineIKCVList = pm.ls('{}.cv[*]'.format(jntsplineIK[2]),fl=True)
	splineIKCVListNum = len(splineIKCVList)
	for i in range(splineIKCVListNum):
		cvcluster = pm.cluster(splineIKCVList[i],n='cv_cluster{}'.format(i+1))[1]
		clusterList.append(cvcluster)
			
def stretchSplineIKIKJnt(jntChain,splineIKCurve):
	pass
	
creatJoint(11,5)	
creatSplineIK(jntChain,5)