Program myProgCorrect

var x : int
var y : float
var z : int[5+2]

main()
{
    x = y-1 * (2.4+400)-3 / 2*y
    when ( z>2*x) then {
	  z = z-2*x
        write(z)
    }    
    write(x)
    y = read()
    write("hola")
    y = 2+x*y
    when ( x+4>2*y) then {
	  z = 2*x
        write(y)
    } else {
	  z = 2/x
    }
}