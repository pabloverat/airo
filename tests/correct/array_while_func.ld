Program array_search

var i : int
var j : int
var arr : int[1:10]

func print_arr() : void
{
	i = 1
	while(i<=10) then 
	{
		write(arr[i])
		i = i+1
	}
}

main ()
{
	i = 1
	while(i<=10) then 
	{
		arr[i] = i+1
		i = i+1
	}
	print_arr()
	j = 5
	
}