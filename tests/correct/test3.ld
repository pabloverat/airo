Program myProgCorrect

var x : float
var y : float
var z : float
var A : int
var B : int
var C : int
var D : int


main()
{
    y = 2.0
    x = y-1 * (2.4+400)-3 / 2*y
    z = x - 1
    when ( z>2*x) then {
	  z = z-2*x
        write(z)
    }    
    write(x)
    y = read()
    write("hola")
    y = 2+x*y

    A = 1
    B = 2
    C = 3
    D = 4
    when (A + B < C) then
    {
        A = B + C
        while (A > B + C) then
        {
            A = A - 1
        }
    } else
    {
        while (B < C + D) then
        {
            B = B+1
	    write(B)
        }
    }

    write("-------")
    write(A)
    write(B)
    write(C)
}