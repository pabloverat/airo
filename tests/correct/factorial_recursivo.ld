Program factorial_ciclo

var n: int
var f: int
var i: int

func factorial(n: int): int
{
    var result : int
    var temp : int

    when (n == 0) then{
        result = 1
    } else {
	temp = factorial(n-1)
        result = n * temp
    }

    return result
}

main()
{
    n = 6
    f = factorial(n)

    write("El factorial de")
    write(n)
    write("es ")
    write(f)
}

