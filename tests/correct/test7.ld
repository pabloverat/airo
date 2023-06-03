Program myProgram

var x : int
var y : float

main()
{
    x = 2+3*2
    y = x*5/(x-2)
    write(y)
    while (y>0) then {
	    write(y)
	    y = y-1
    }

}