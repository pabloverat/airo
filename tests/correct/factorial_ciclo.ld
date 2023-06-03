Program factorial_ciclo

var n: int
var f: int
var i: int

main()
{
    n = 6
    f = 1
    i = 1
    while ( i<=n ) then {
        f = f * i
        i = i + 1
    }
    write("El factorial de")
    write(n)
    write("es ")
    write(f)
}

