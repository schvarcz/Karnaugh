from pyIbex import *
from vibes import *
import time


vibes.beginDrawing()
vibes.newFigure("Karnaugh2")
vibes.setFigureProperties({"x":100, "y": 100, "width": 1300, "height": 800})



X0 = IntervalVector([[-20,20], [-20,20]])
lands = [[10,-10],[-10,10]]

f = Function("x","y","1.2*x-y")

seps = []
contractors = []

#Contractor
C = CtcFwdBwd(f,Interval(0,0))
b = IntervalVector(2)
b[0], b[1] = X0[0], X0[1]
C.contract(b)
x,y = b[0], b[1]
vibes.drawBox(x.lb(), x.ub(), y.lb(), y.ub(),"blue")
contractors.append(C)


#Separator
sep = SepFwdBwd(f,Interval(-1,1))
res_in , res_out, res_y = pySIVIA(X0,sep,0.5,color_out="",color_in="k[blue]")
seps.append(sep)

for x0,y0 in lands:

	#Contractor
	f = Function("x","y","sqrt((x-{0})^2+(y-{1})^2)".format(x0,y0))
	C = CtcFwdBwd(f,Interval(-1,5))
	b = IntervalVector(2)

	b[0], b[1] = X0[0], X0[1]
	C.contract(b)
	x,y = b[0], b[1]
	vibes.drawBox(x.lb(), x.ub(), y.lb(), y.ub(),"blue")
	contractors.append(C)

	#Separator
	sep = SepFwdBwd(f,Interval(-1,5))
 	
	res_in , res_out, res_y = pySIVIA(X0,sep,0.5,color_out="",color_in="k[blue]")
	seps.append(sep)


C = contractors[1]
b = IntervalVector(2)
b[0], b[1] = X0[0], X0[1]
C.contract(b)
x,y = b[0], b[1]
vibes.drawBox(x.lb(), x.ub(), y.lb(), y.ub(),"yellow")

C = contractors[2]
b = IntervalVector(2)
b[0], b[1] = X0[0], X0[1]
C.contract(b)
x,y = b[0], b[1]
vibes.drawBox(x.lb(), x.ub(), y.lb(), y.ub(),"green")

C = (contractors[1] | contractors[2]) & contractors[0]
b = IntervalVector(2)
b[0], b[1] = X0[0], X0[1]
C.contract(b)
x,y = b[0], b[1]
vibes.drawBox(x.lb(), x.ub(), y.lb(), y.ub(),"red")

C = (contractors[1] & contractors[0]) | (contractors[2] & contractors[0])
b = IntervalVector(2)
b[0], b[1] = X0[0], X0[1]
C.contract(b)
x,y = b[0], b[1]
print(b)
vibes.drawBox(x.lb(), x.ub(), y.lb(), y.ub(),"green")


# C = (contractors[1]&contractors[2])
# C.contract(b)
# vibes.drawBox(x.lb(), x.ub(), y.lb(), y.ub(),"red")
# C1.contract(b)
# x,y = b[0], b[1]
# vibes.drawBox(x.lb(), x.ub(), y.lb(), y.ub(),"yellow")
# C2.contract(b)
# x,y = b[0], b[1]
# vibes.drawBox(x.lb(), x.ub(), y.lb(), y.ub(),"green")

# res_in , res_out, res_y = pySIVIA(X0,C,0.5,color_out="",color_in="k[blue]")

# res_in , res_out, res_y = pySIVIA(X0,(seps[0]|seps[1])&seps[2],0.5,color_out="",color_in="k[blue]")
# res_in , res_out, res_y = pySIVIA(X0,seps[0]|seps[1]&seps[2],0.5,color_out="",color_in="k[green]")
# pySIVIA(X0,C,0.5)