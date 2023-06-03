Program myProgCorrect

var w : int
var x : int
var y : float[5][6]

func myFoo() : void
{
    var a : char
    var b : float
    
    b = read()
    b = x + 41.0 * (33-22.4/2+4*13)
    write(b)
}

main()
{
    x = 1
    y = 2.0 
    write(x)
    when (y!=x) then
    {
        myFoo()
    }
}