Program myProgCorrect

var x : int
var y : float
var z : bool

func myFoo() : void
{
    var a : char
    var b : int
    
    a = read()
    b = x + 41 
}

func myFoo2(x : int, y : float) : int
{
    var m : int
    var n : float

    while (m > x OR n < y) then
    {
        m = m - 1
        n = n + 1.5
    }

    return m
}

main()
{
    y = 2
    x = y - 1
    write(x)
    when (y>x) then
    {
        myFoo()
    }
    y = myFoo2(x, myFoo2(x, y))
}