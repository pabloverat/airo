Program myProgCorrect

var x : int
var y : float
var z : int[5]

main()
{
    y = 2
    x = y - 1
    write(z[x])
    when (FALSE AND x>2) then {
        write(y)
    }
}