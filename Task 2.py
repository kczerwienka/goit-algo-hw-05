import numpy as np

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    i = 0

    while low <= high:
        i += 1

        mid = (high + low) // 2
 
        # if x is greater than the value in the middle of the list, ignore the left half
        if arr[mid] < x:
            low = mid + 1
 
        # if x is less than the value in the middle of the list, ignore the right half
        elif arr[mid] > x:
            high = mid - 1
 
        # otherwise x is present at the position and returns it
        else:
            return (i, arr[high])
 
    # if the element is not found
    return -1


arr = np.array([2, 3, 4, 10, 40]) / 100
x = 10 / 100
result = binary_search(arr, x)
if result != -1:
    print(f"Element is present at index {result[0]}, smallest element that is greater than or equal to the given value {result[1]}")
else:
    print("Element is not present in array")

