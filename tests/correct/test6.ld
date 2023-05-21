Program patito

var i : int
var j : int
var k : int
var f : float

func uno(a: int, b: int) : void {
	when (a>0) then
	{
		i = a+b*j+i
		write( i+j )
	} else {
		write( a+b )	
	}
}

func dos(a: int, g: float) : void {
	var i : int
	i=a
	while (a>0) then {
		a= a-k*j
		uno(a*2, a+k)
		g=g*j-k
	}
}

main() {
	i=2
	k=i+1
	f=3.14
	while (i>0) then {
		dos(i+k, f*3)
		write(i)
		write(j*2)
		write(f*2+1.5)
		i=1-k/2
	}
}