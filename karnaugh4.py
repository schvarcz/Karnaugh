from pyIbex import *
from vibes import *


vibes.beginDrawing()
vibes.newFigure("Karnaugh4")
vibes.setFigureProperties({"x":100, "y": 100, "width": 1300, "height": 800})



X0 = IntervalVector([[-40,40], [-40,40]])
lands = [[2,2,10],[15,2,10],[2,-5,10],[15,-5,10]]

seps = []
for x0,y0,r in lands:
	print("sqrt((x-{0})^2+(y-{1})^2) < {2}".format(x0,y0,r))

	#Contractor
	f = Function("x","y","sqrt((x-{0})^2+(y-{1})^2)".format(x0,y0))
	C = CtcFwdBwd(f,Interval(-1,r))
	b = IntervalVector(2)

	b[0], b[1] = X0[0], X0[1]
	C.contract(b)
	x,y = b[0], b[1]

	#Separator
	sep = SepFwdBwd(f,Interval(-1,r))
 	
	res_in , res_out, res_y = pySIVIA(X0,sep,1,color_out="")
	seps.append(sep)

	sep = SepFwdBwd(f,Interval(r,float("inf")))
	seps.append(sep)

A, _A, B, _B, C, _C, D, _D = seps

# 2 Groups
sep = ( A & B & C & D ) | ( A & _B & C & D ) | ( A & B & C & _D ) | ( A & _B & C & _D )

sep = ( A & C & D ) | ( A & B & C & _D ) | ( A & _B & C & _D )
sep = ( A & B & C & D ) | ( A & _B & C & D ) | ( A & C & _D )
sep = ( A & B & C ) | ( A & _B & C & D ) | ( A & _B & C & _D )
sep = ( A & B & C & D ) | ( A & _B & C ) | ( A & B & C & _D )

sep = ( A & C & D ) | ( A & C & _D )
sep = ( A & B & C ) | ( A & _B & C )

sep = ( A & B & C ) | ( A & C & D ) | ( A & C & _D )
sep = ( A & _B & C ) | ( A & C & D ) | ( A & C & _D )
sep = ( A & B & C ) | ( A & _B & C ) | ( A & C & D )
sep = ( A & B & C ) | ( A & _B & C ) | ( A & C & _D )

sep = ( A & B & C ) | ( A & _B & C ) | ( A & C & D ) | ( A & C & _D )

# sep = ( A & C )


# 3 Groups
sep = ( A & B & C & D ) | ( A & B & C & _D )

# sep = ( A & B & C )


#Any combination of 2 or 3 groupsX
sep = ( _A & C & D ) | ( _B & C & D ) | ( A & _B & C ) | ( A & C & _D ) | ( A & B & _D ) | ( A & B & _C ) | ( B & _C & D ) | ( _A & B & D )



res_in , res_out, res_y = pySIVIA(X0,sep,0.5,color_out="",color_in="k[blue]")

