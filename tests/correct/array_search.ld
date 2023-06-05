Program array_search

var i : int
var j : int
var arr : int[1:10]

func arr_search() : void
{
	i = 1
	while(i<=10) then 
	{
		when(arr[i] == 4) then
		{
			j = arr[i]
		}
		i = i+1
	}
	write(j)
}

main ()
{
	i = 1
	while(i<=10) then 
	{
		arr[i] = i+1
		i = i+1
	}
	arr_search()
	j = 5
	
}