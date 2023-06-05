Program array_search

var i : int
var j : int
var arr : int[1:10]

main ()
{
	i = 10
	while(i>=0) then 
	{
		arr[i] = i
		i = i-1
	}
	i = 1
	while(i<=10) then 
	{
		write(arr[i])
		i = i+1
	}
}