from pyIbex import *
from vibes import *

from collections import deque
vibes_available= True

class Sep():
	def __init__(self, cin, cout):
		self.cin = cin
		self.cout = cout

	def separate(self,X):
		XA = IntervalVector(X)
		XB = IntervalVector(X)
		
		self.cin.contract(XA)
		self.cout.contract(XB)
		yout, ymaybe, yin = X.diff(XA), [XA&XB], XA.diff(XB)


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



def SIVIA_ctc(X0, ctcIn, ctcOut, epsilon, color_in='k[b]', color_out='k[]', color_maybe='k[y]', draw_boxes=True, save_result=True, **kwargs):

	stack =  deque([IntervalVector(X0)])
	res_y = []; res_out = []
	lf = LargestFirst(epsilon/2.0)
	k = 0

	while len(stack) > 0:
		k = k+1
		X = stack.popleft()

		XA = IntervalVector(X)
		XB = IntervalVector(X)
		
		ctcIn.contract(XA)
		ctcOut.contract(XB)

		if (draw_boxes == True and vibes_available == True):
			drawBoxDiff(X,XA,color_out, **kwargs)

		if save_result == True:
			res_out += X.diff(XA)
		
		if XA.is_empty():
			continue
		else:
			for b in XA.diff(XB):
				vibes.drawBox(b[0].lb(), b[0].ub(),b[1].lb(), b[1].ub(), color_in)

			Xmaybe = XA&XB
			if Xmaybe.is_empty():
				continue
			if Xmaybe.max_diam() < epsilon:
				if draw_boxes == True:
					vibes.drawBox(Xmaybe[0].lb(), Xmaybe[0].ub(),Xmaybe[1].lb(), Xmaybe[1].ub(), color_maybe)
				if save_result == True:
					res_y.append(Xmaybe)
			elif (Xmaybe.is_empty() == False):
					(X1, X2) = lf.bisect(Xmaybe)
					stack.append(X1)
					stack.append(X2)


	print('nb contraction %d / nombre de boite %d'%(k,len(res_out)+len(res_y)))

	return (res_out, res_y)


def SIVIA_msep(X0, sep, epsilon, color_in='k[b]', color_out='k[]', color_maybe='k[y]', draw_boxes=True, save_result=True, **kwargs):

	stack =  deque([IntervalVector(X0)])
	res_y = []; res_out = []
	lf = LargestFirst(epsilon/2.0)
	k = 0

	while len(stack) > 0:
		k = k+1
		X = stack.popleft()

		X0 = IntervalVector(X)
		
		yout, ymaybe, yin = sep.separate(X0)

		if (draw_boxes == True and vibes_available == True):
			drawBoxDiff(X,XA,color_out, **kwargs)

		if save_result == True:
			res_out += X.diff(XA)
		
		if XA.is_empty():
			continue
		else:
			Xmaybe = XA&XB
			for b in yin:
				vibes.drawBox(b[0].lb(), b[0].ub(),b[1].lb(), b[1].ub(), color_in)

			if Xmaybe.is_empty():
				continue
			elif Xmaybe.max_diam() < epsilon:
				if draw_boxes == True:
					vibes.drawBox(Xmaybe[0].lb(), Xmaybe[0].ub(),Xmaybe[1].lb(), Xmaybe[1].ub(), color_maybe)
				if save_result == True:
					res_y.append(Xmaybe)
			elif (Xmaybe.is_empty() == False):
					(X1, X2) = lf.bisect(Xmaybe)
					stack.append(X1)
					stack.append(X2)


	print('nb contraction %d / nombre de boite %d'%(k,len(res_out)+len(res_y)))

	return (res_out, res_y)


vibes.beginDrawing()
vibes.newFigure("Karnaugh5-1")
vibes.setFigureProperties({"x":100, "y": 100, "width": 800, "height": 800})



X0 = IntervalVector([[-40,40], [-40,40]])
# X0 = IntervalVector([[-5,20], [-4,8]])
lands = [[2,2,10],[15,2,10],[2,-5,10],[15,-5,10]]

conts = []
seps = []
for x0,y0,r in lands:
	# r = Interval(r-2,r+2)
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


A, _A, B, _B, C, _C, D, _D = conts

# X = ( A & C & D ) | ( A & B & C ) | ( A & B & _C ) | ( A & _B & _C & _D ) | ( _A & _C & D ) | ( _A & B & _C )
# _X = ( _A | _C | _D ) & ( _A | _B | _C ) & ( _A | _B | C ) & ( _A | B | C | D ) & ( A | C | _D ) & ( A | _B | C )

# SIVIA_ctc(X0,X,_X,0.1,color_out="[]",color_in="k[#818181]",color_maybe="white[white]")

# X = ( _A & C & D ) | ( _A & B & C ) | ( _A & C & _D ) | ( _A & _B & _D ) | ( A & _B & C & _D ) | ( A & _B & _C & D ) 
# _X = ( A | _C | _D ) & ( A | _B | _C ) & ( A | _C | D ) & ( A | B | D ) & ( _A | B | _C | D ) & ( _A | B | C | _D ) 

# SIVIA_ctc(X0,X,_X,0.1,color_out="k[]",color_in="k[#aaaaaa]",color_maybe="white[white]")



X = ( A & C & D ) | ( A & B ) | ( A & _C & _D ) | ( _A & _C & D ) | ( B & _C )
_X = ( _A | _C | _D ) & ( _A | _B ) & ( _A | C | D ) & ( A | C | _D ) & ( _B | C )
SIVIA_ctc(X0,X,_X,0.1,color_out="[]",color_in="k[#818181]",color_maybe="white[white]")


X = ( _A & C ) | ( _B & C & _D ) | ( _A & _B & _D ) | ( A & _B & _C & D )
_X = ( A | _C ) & ( B | _C | D ) & ( A | B | D ) & ( _A | B | C | _D )
SIVIA_ctc(X0,X,_X,0.1,color_out="[]",color_in="k[#aaaaaa]",color_maybe="white[white]")

