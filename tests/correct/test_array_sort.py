arr = [None]*5

def print_arr(n: int):
    i = 0
    while (i < n):
        print(arr[i])
        i = i+1

def bubbleSort(n: int):
    i=0
    while (i < n-1):
        j=1
        while (j < n-1):
            if (arr[j]>arr[j+1]):
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp
            j = j+1
        i = i+1

def main():
    i = 0
    n = 5

    print("Unsorted array: ")
    while (i < n):
        arr[i] = n-i
        print(arr[i])
        i = i+1

    bubbleSort(n)
    print("Sorted array: ")
    print_arr(n)


if __name__ == "__main__":
    main()