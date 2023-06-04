Program myProgCorrect

var w : int
var x : int
var y : float[5][6]

func myFoo(c: int, b: float) : void
{
    var a : float
    
    a = b + 41.0 * (c-22.4/2+4*13)
    write(a)
}

main()
{
    x = 1
    write(x)
    y = read()
    w = 33
    when (y!=x) then
    {
        myFoo(w, y)
    }
}