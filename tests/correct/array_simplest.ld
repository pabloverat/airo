Program arraySimplest

var a : int[1:2][3:5]
var b : int[5:8]
var y : int

main()
{
    y = 5
    a[1][4] = 10*2
    b[8] = a[1][4]*2
    write(a[1][4])
    write(b[8])	
    write("adiós")
}