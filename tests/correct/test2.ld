Program myProgCorrect

var x : float
var y : float
var z : float
var a : int
var b : int

main()
{
    write("hola")
    y = 2*1.0
    x = y-1 * (2.4+400)-3 / 2*y
    z = 3*1.0
    when ( z>2*x) then {
	  z = z-2*x
        write(z)
    }    
    write(x)
    y = read()
    write("hola")
    y = 2+x*y
    when ( x+4>2*y) then {
	  a = 2
        write(a)
    } else {
	  z = 2/x
    }
}