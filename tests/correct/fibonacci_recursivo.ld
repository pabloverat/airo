Program Fibonacci

var nterms : int
var idx : int
var fibo : int

func recur_fibo(n:int) : int
{
    var result : int
    var temp : int

    when (n <= 1) then
    {
        result = n
    }else
    {
	    temp = recur_fibo(n-1)
        result = temp + recur_fibo(n-2)
    }
    return result
}

main()
{
    nterms = 5
    idx = 0
    when (nterms <= 0) then
    {
        write("Plese enter a positive integer")
    } else
    {
        write("Fibonacci sequence:")
        while (idx < nterms ) then
        {
	    fibo = recur_fibo(idx)
            write(fibo)
            idx = idx+1
	    write("---")
        }
    }
}