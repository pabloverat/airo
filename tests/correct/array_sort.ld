Program arrSort

var i : int
var n : int
var arr : int[0:4]

func print_arr(n: int) : void
{
    i = 0
    while (i < n) then
    {
        write(arr[i])
        i = i+1
    }
}

func bubbleSort(n: int): void
{
    var i: int
    var j: int
    var temp: int

    i=0
    
    while (i < n-1) then
    {
        j=0
        while (j < n-i-1) then
        {
            when (arr[j]>arr[j+1]) then
            {
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp
            }
            j = j+1
        }
        i = i+1
    }   
}

main()
{
    i = 0
    n = 5

    write("Unsorted array: ")
    while (i < n) then
    {
        arr[i] = n-i
        write(arr[i])
        i = i+1
    }

    bubbleSort(n)
    write("Sorted array: ")
    print_arr(n)
}