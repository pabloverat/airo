Program fibonacci_ciclo

var a:int
var b:int
var c:int
var cont:int
var num:int

main()
{
    a = 0
    b = 1
    c = 0
    cont = 0
    num = 20
    while( cont<num ) then {
        write(c)
        a = b
        b = c
        c = a + b
        cont = cont + 1
    }
}