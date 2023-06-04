Program myProgCorrect

var w : int
var x : int
var y : float[5][6]


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
}