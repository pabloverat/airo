Program myProgCorrect

var w : float
var x : int
var y : float[5][6]

func entrediez(i: float) : float
{
    i = i/10
    return i
}

func pordiez(i: int) : int
{
    i = i*10
    return i
}

main()
{
    x = 4
    x = pordiez(x-1)
    write(x)
    w = 5 * 12.2
    w = entrediez(w)
    write(w)
}