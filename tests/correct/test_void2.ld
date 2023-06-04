Program myProgCorrect

var w : int
var x : int
var y : float[5][6]


func hola(i: int) : void
{
    write(i)
    when ( i>0) then
    {
	hola(i-1)
    }
    write(i)
}

main()
{
    x = 6
    hola(x-1)
}