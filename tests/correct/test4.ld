Program myProgCorrect

var w : int
var x : int
var y : float[5+2][6]

func myFoo() : void
{
    var a : char
    var b : float
    
    b = read()
    b = x + 41.0 * (33-22.4/2+4*13)
    write(b)
}

func myFoo2(x : int, y : float) : float
{
    var m : int
    var n : float

    while (m > x) then
    {
        m = m - 1
        n = n + 1.5
    }

    return n + 2
}

func myFoo3(m: int) : float
{
    var n : float

    write("hello")
    return myFoo2(m, 4.5)*2
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
    y = myFoo2(x, myFoo2(x, y))
}