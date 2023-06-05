Program mmult

var a : float[0:2][0:2]
var b : float[0:2][0:2]
var c : float[0:2][0:2] 
var acols : float
var arows : float
var bcols : float
var brows : float

var i : int
var j : int
var k : int

func fillMatrices() : void
{
    i = 0
    while(i < arows) then
    {
        j = 0
        while(j < acols) then
        {
            a[i][j] = read()
            j = j+1
        }
        i = i+1
    }
    i = 0
    while(i < brows) then
    {
        j = 0
        while(j < bcols) then
        {
            b[i][j] = read()
            j = j+1
        }
        i = i+1
    }
}

func multMatrices() : void
{
    i = 0
    while(i < arows) then
    {
        j = 0
        while(j < bcols) then
        {
            k=0
            while(k < brows) then
            {
                c[i][j] = c[i][j] + (a[i][k] * b[k][j])
                k = k+1
            }
            j = j+1
        }
        i = i+1
    }
}

main()
{
    i = 0
    j = 0
    k = 0

    arows = 3.0
    acols = 3.0
    brows = 3.0
    bcols = 3.0


    while (i<3) then {
        j = 0
        while (j < 2)
    }
}