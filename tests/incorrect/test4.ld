Program myProgCorrect

var x : int
var y : float

func myFoo() : void
{
    var a : char
    var b : int
    
    a = read()
    b = x + 41 
}

func myFoo(x : int, y : float) : int
{
    var m : int
    var m : float

    while (m > x) then
    {
        m = m - 1
        n = n + 1.5
    }

    return m + myFoo2(m, n)*2
}

main()
{
    y = 2
    x = y - 1
    write(x)
    when (y!=x) then
    {
        myFoo()
    }
    y = myFoo2(x, myFoo2(x, y))
}