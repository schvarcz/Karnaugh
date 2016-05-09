from pyIbex import *
from vibes import *	
from mSivia import *
import time


def test1():
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


def test2():
	""" Example of fake boundaring using separators """
	vibes.beginDrawing()
	vibes.newFigure("Karnaugh2")
	vibes.setFigureProperties({"x":100, "y": 100, "width": 1300, "height": 800})

	X0 = IntervalVector([[-40,40], [-40,40]])

	lands = [[2,2,10],[2,2,5],[18,2,10],[18,2,5]]
	conts, seps = ctcsAndSeps(lands)

	B, _B, A, _A, D, _D, C, _C = seps

	sep = (_A & B & _C & D) | (_A & B & _C & _D) | (_A & _B & _C & D)
	sep =  (_A & B & _C) | (_A & _B & _C & D)
	# sep =  (_A & B & _C & _D) | (_A & _C & D)
	sep =  (_A & B & _C) | (_A & _C & D)
	res_in , res_out, res_y = pySIVIA(X0,sep,0.5,color_out="",color_in="k[blue]")


def test3():
	""" Example of only fake boundaring using separators """
	vibes.beginDrawing()
	vibes.newFigure("Karnaugh3")
	vibes.setFigureProperties({"x":100, "y": 100, "width": 1300, "height": 800})

	X0 = IntervalVector([[-40,40], [-40,40]])

	lands = [[2,2,10],[18,2,10],[10,-10,10]]
	conts, seps = ctcsAndSeps(lands)

	A, _A, B, _B, C, _C = seps

	sep = ( A & B & C ) | ( A & _B & C ) | (_A & B & C )
	sep = ( A & C ) | (_A & B & C )
	sep = ( A & _B & C ) | ( B & C ) 
	sep = ( A & C ) | ( B & C ) 

	sep = (A & _B & C) | (A & _B & _C) | (_A & B & C) | (_A & B & _C)
	sep = (A & _B) | (_A & _B)
	sep = (C & _B) | (_C & _B)
	res_in , res_out, res_y = pySIVIA(X0,sep,0.5,color_out="",color_in="k[blue]")


def test4():
	""" Example of fake boundaring using separators """
	vibes.beginDrawing()
	vibes.newFigure("Karnaugh4-1")
	vibes.setFigureProperties({"x":100, "y": 100, "width": 1600, "height": 800})

	X0 = IntervalVector([[-40,40], [-40,40]])

	lands = [[2,2,10],[15,2,10],[2,-5,10],[15,-5,10]]
	conts, seps = ctcsAndSeps(lands)

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
	# X = ( _A & C & D ) | ( _B & C & D ) | ( A & _B & C ) | ( A & C & _D ) | ( A & B & _D ) | ( A & B & _C ) | ( B & _C & D ) | ( _A & B & D )

	# X = ( A & C & D ) | ( A & B & C ) | ( A & B & _C ) | ( A & _B & _C & _D ) | ( _A & _C & D ) | ( _A & B & _C )
	# _X = ( A & _B & C & _D ) | ( A & _B & _C & D ) | ( _A & C & D ) | ( _A & C & D ) | ( _A & B & C ) | ( _A & C & _D ) | ( _A & _B &_D )

	X = ( A & _B ) | ( _A & B ) | ( A & B )
	_X = ( _A & _B )

	X = ( A & _B ) | ( A & B )

	pySIVIA(X0,X,0.5,color_out="k[]",color_in="k[#818181]",color_maybe="k[yellow]")
	# pySIVIA(X0,X,0.5,color_out="k[]",color_in="k[#818181]",color_maybe="white[white]")
	# pySIVIA(X0,_X,0.5,color_out="k[]",color_in="k[#aaaaaa]",color_maybe="white[white]")

	# sep = SepCtcPair(X,_X)
	# pySIVIA(X0,sep,0.5,color_out="k[]",color_in="k[#929292]",color_maybe="white[white]")
	vibes.saveImage("true.svg")


def test5():
	""" Example of fake boundaring using contractors """
	vibes.beginDrawing()
	vibes.newFigure("Karnaugh5-1")
	vibes.setFigureProperties({"x":100, "y": 100, "width": 800, "height": 800})

	X0 = IntervalVector([[-40,40], [-40,40]])
	# X0 = IntervalVector([[-5,20], [-4,8]])

	lands = [[2,2,10],[15,2,10],[2,-5,10],[15,-5,10]]
	conts, seps = ctcsAndSeps(lands)


	A, _A, B, _B, C, _C, D, _D = conts

	X1 = ( A & C & D ) | ( A & B & C ) | ( A & B & _C ) | ( A & _B & _C & _D ) | ( _A & _C & D ) | ( _A & B & _C )
	_X1 = ( _A | _C | _D ) & ( _A | _B | _C ) & ( _A | _B | C ) & ( _A | B | C | D ) & ( A | C | _D ) & ( A | _B | C )

	# SIVIA_ctc(X0,X1,_X1,0.1,color_out="[]",color_in="k[#818181]",color_maybe="white[white]")

	X2 = ( A & _B & C & _D ) | ( A & _B & _C & D ) | ( _A & C & D ) | ( _A & B & C ) | ( _A & C & _D ) | ( _A & _B & _D )
	_X2 = ( A | _C | _D ) & ( A | _B | _C ) & ( A | _C | D ) & ( A | B | D ) & ( _A | B | _C | D ) & ( _A | B | C | _D ) 

	SIVIA_ctc(X0,_X2,_X1,0.1,color_out="k[blue]",color_in="k[red]",color_maybe="k[yellow]")

	# X = ( A & C & D ) | ( A & B ) | ( A & _C & _D ) | ( _A & _C & D ) | ( B & _C )
	# _X = ( _A | _C | _D ) & ( _A | _B ) & ( _A | C | D ) & ( A | C | _D ) & ( _B | C )
	# SIVIA_ctc(X0,X,_X,0.1,color_out="[]",color_in="k[#818181]",color_maybe="white[white]")

	# _X = ( _A & C ) | ( _B & C & _D ) | ( _A & _B & _D ) | ( A & _B & _C & D )
	# _X = ( A | _C ) & ( B | _C | D ) & ( A | B | D ) & ( _A | B | C | _D )
	# SIVIA_ctc(X0,X,_X,0.1,color_out="[]",color_in="k[#818181]",color_maybe="white[white]")

	# pySIVIA(X0,X,0.5,color_maybe="k[blue]")
	# pySIVIA(X0,_X2,0.5,color_maybe="k[yellow]")
	# SIVIA_ctc(X0,_B,B,0.1,color_out="[]",color_in="k[#aaaaaa]",color_maybe="k[yellow]")


def test6():
	""" A complete example of fake boundaring using contractors and three sets """
	X0 = IntervalVector([[-40,40], [-40,40]])

	lands = [[2,2,10],[15,2,10],[8,-5,10]]
	conts, seps = ctcsAndSeps(lands)

	A, _A, B, _B, C, _C = conts

	X1 = ( A & B ) | ( A & _B )
	_X1 = ( _A | _B ) & ( _A | B )

	X2 = ( _A & C ) | ( _A & _C )
	_X2 = ( A | _C ) & ( A | C )

	X3 =  _A & ( C | _C )
	_X3 = A | ( C & _C )

	#Drawing
	vibes.beginDrawing()

	vibes.newFigure("Karnaugh6-1")
	vibes.setFigureProperties({"x":100, "y": 100, "width": 800, "height": 400})
	SIVIA_ctc(X0,X1,_X1,0.1,color_out="k[blue]",color_in="k[red]",color_maybe="k[yellow]")

	vibes.newFigure("Karnaugh6-2")
	vibes.setFigureProperties({"x":1000, "y": 100, "width": 800, "height": 400})
	SIVIA_ctc(X0,_X2,X2,0.1,color_out="k[blue]",color_in="k[red]",color_maybe="k[yellow]")
	
	vibes.newFigure("Karnaugh6-3")
	vibes.setFigureProperties({"x":100, "y": 600, "width": 800, "height": 400})
	SIVIA_ctc(X0,_X3,X3,0.1,color_out="k[blue]",color_in="k[red]",color_maybe="k[yellow]")

	vibes.newFigure("Karnaugh6-4")
	vibes.setFigureProperties({"x":1000, "y": 600, "width": 800, "height": 400})
	SIVIA_ctc(X0,X2,_X1,0.1,color_out="k[blue]",color_in="k[red]",color_maybe="k[yellow]")

	vibes.newFigure("Karnaugh6-5")
	vibes.setFigureProperties({"x":550, "y": 350, "width": 800, "height": 400})
	SIVIA_ctc(X0,X5,_X5,0.1,color_out="k[blue]",color_in="k[red]",color_maybe="k[yellow]")


if __name__ == "__main__":
	test6()