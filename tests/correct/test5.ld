Program myProgCorrect

var x : int
var y : float[3]
var f : frame

func myFoo() : int
{
    var a : char[10]
    var b : int
    
    a = read()
    b = 41 + x

    return b
}

func ciclos(A:int, B:int, C:float, D:frame) : frame
{
    when (A + B < C) then
    {
        A = B + C
        while (A > B + C) then
        {
            A = A - 1
        }
    } else
    {
        while (B > C + D) then
        {
            A = B + C * D
            B = A-D
        }
    }
    A = B*C
    return myFoo(myFoo(A+B*C), A)
}

main()
{
    y[1] = 2
    x = y[2] - 1
    write(x)
    when (y[1]+y[2]>x) then
    {
        myFoo()
        f = ciclos(y[1], x, 3, 41)
    }
}