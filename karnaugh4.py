from pyIbex import *
from vibes import *

from collections import deque
vibes_available= True

def drawBoxDiff(X0, X, color, use_patch=False, **kwargs):
	if X0 == X: return
	if not X.is_empty():
		if use_patch == True:
			vibes.drawBoxDiff([X0[0].lb(), X0[0].ub(), X0[1].lb(), X0[1].ub()],
			 [X[0].lb(), X[0].ub(), X[1].lb(), X[1].ub()], color)
		else:
			for b in X0.diff(X):
				vibes.drawBox(b[0].lb(), b[0].ub(), b[1].lb(), b[1].ub(), color)	
	else:
		vibes.drawBox(X0[0].lb(), X0[0].ub(), X0[1].lb(), X0[1].ub(), color)

def SIVIA_ctc(X0, ctc, epsilon, color_in='k[b]', color_out='k[]', color_maybe='k[y]', draw_boxes=True, save_result=True, **kwargs):

	stack =  deque([IntervalVector(X0)])
	res_y = []; res_out = []
	lf = LargestFirst(epsilon/2.0)
	k = 0

	while len(stack) > 0:
		k = k+1
		X = stack.popleft()
		X0 = IntervalVector(X)

		#X =  __contract_and_extract(X, ctc, res_out, color_out)
		ctc.contract(X)
		if (draw_boxes == True and vibes_available == True):
			drawBoxDiff(X0,X,color_out, **kwargs)

		if save_result == True:
			res_out += X0.diff(X)


		if (X.is_empty()):
			# vibes.drawBox(X0[0].lb(), X0[0].ub(),X0[1].lb(), X0[1].ub(), color_in)
			continue
		if( X.max_diam() < epsilon):
			if draw_boxes == True:
				vibes.drawBox(X[0].lb(), X[0].ub(),X[1].lb(), X[1].ub(), color_maybe)
			if save_result == True:
				res_y.append(X)
		elif (X.is_empty() == False):
			if X0 == X:
				vibes.drawBox(X[0].lb(), X[0].ub(),X[1].lb(), X[1].ub(), color_in)
			else:
				(X1, X2) = lf.bisect(X)
				stack.append(X1)
				stack.append(X2)


	print('nb contraction %d / nombre de boite %d'%(k,len(res_out)+len(res_y)))

	return (res_out, res_y)


vibes.beginDrawing()
vibes.newFigure("Karnaugh4-1")
vibes.setFigureProperties({"x":100, "y": 100, "width": 800, "height": 800})



X0 = IntervalVector([[-40,40], [-40,40]])
lands = [[2,2,10],[15,2,10],[2,-5,10],[15,-5,10]]

seps = []
conts = []
for x0,y0,r in lands:
	print("sqrt((x-{0})^2+(y-{1})^2) < {2}".format(x0,y0,r))
	f = Function("x","y","sqrt((x-{0})^2+(y-{1})^2)".format(x0,y0))

	#Contractor
	C = CtcFwdBwd(f,Interval(-1,r))
	conts.append(C)
	# res_in , res_out, res_y = pySIVIA(X0,C,1,color_out="k[gray]",color_in="k[blue]",color_maybe="k[red]")
	C = CtcFwdBwd(f,Interval(r,float("inf")))
	conts.append(C)

	#Separator
	sep = SepFwdBwd(f,Interval(-1,r))
	# res_in , res_out, res_y = pySIVIA(X0,sep,1,color_out="",color_in="k[#A9A9A9]",color_maybe="k[white]")
	seps.append(sep)
	sep = SepFwdBwd(f,Interval(r,float("inf")))
	seps.append(sep)

A, _A, B, _B, C, _C, D, _D = seps

# 2 Groups
# X = ( A & B & C & D ) | ( A & _B & C & D ) | ( A & B & C & _D ) | ( A & _B & C & _D )

# X = ( A & C & D ) | ( A & B & C & _D ) | ( A & _B & C & _D )
# X = ( A & B & C & D ) | ( A & _B & C & D ) | ( A & C & _D )
# X = ( A & B & C ) | ( A & _B & C & D ) | ( A & _B & C & _D )
# X = ( A & B & C & D ) | ( A & _B & C ) | ( A & B & C & _D )

# X = ( A & C & D ) | ( A & C & _D )
# X = ( A & B & C ) | ( A & _B & C )

# X = ( A & B & C ) | ( A & C & D ) | ( A & C & _D )
# X = ( A & _B & C ) | ( A & C & D ) | ( A & C & _D )
# X = ( A & B & C ) | ( A & _B & C ) | ( A & C & D )
X = ( A & B & C ) | ( A & _B & C ) | ( A & C & _D )

# X = ( A & B & C ) | ( A & _B & C ) | ( A & C & D ) | ( A & C & _D )
# X = ( A & C )


# 3 Groups
# X = ( A & B & C & D ) | ( A & B & C & _D )
# X = ( A & B & C )


#Any combination of 2 or 3 groupsX
X = ( _A & C & D ) | ( _B & C & D ) | ( A & _B & C ) | ( A & C & _D ) | ( A & B & _D ) | ( A & B & _C ) | ( B & _C & D ) | ( _A & B & D )

X = ( A & C & D ) | ( A & B & C ) | ( A & B & _C ) | ( A & _B & _C & _D ) | ( _A & _C & D ) | ( _A & B & _C )
_X = ( A & _B & C & _D ) | ( A & _B & _C & D ) | ( _A & C & D ) | ( _A & C & D ) | ( _A & B & C ) | ( _A & C & _D ) | ( _A & _B &_D )

X = ( A & _B ) | ( _A & B ) | ( A & B )
_X = ( _A & _B )

pySIVIA(X0,X,0.5,color_out="k[]",color_in="k[#818181]",color_maybe="k[yellow]")
# pySIVIA(X0,X,0.5,color_out="k[]",color_in="k[#818181]",color_maybe="white[white]")
# pySIVIA(X0,_X,0.5,color_out="k[]",color_in="k[#aaaaaa]",color_maybe="white[white]")

# sep = SepCtcPair(X,_X)
# pySIVIA(X0,sep,0.5,color_out="k[]",color_in="k[#929292]",color_maybe="white[white]")
vibes.saveImage("true.svg")

