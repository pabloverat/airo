Program myProgCorrect

var a : int[1:2][3:5]
var b : int[5:8]
var y : int

main()
{
    y = 5
    a[1][4] = 10 * (2+40)-3*y
    write(a[1][4])
    b[8] = 399
    while ( a[1][4]>b[8]) then {
        write(b[8])
        b[8] = b[8] +1
    }    
    write(b[8])	
    write("adiós")
}