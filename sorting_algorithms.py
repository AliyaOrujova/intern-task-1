def insertion_sort(arr):
   
    mylist = arr.copy() # I'm copying the original list to ensure that I don't modify it 

    n = len(mylist) #This is the length of the list 

    for i in range(1, n):#I start from one because if there is a list with one element, there is nothing else that we need to do here
        insert_index = i #This is the index that we will use to keep track of where we should insert the value.
        current_value = mylist[i] #this is what we want to insert into tyhr sorted part 

        for j in range(i - 1, -1, -1): #okay now we are iterating backwards through the part of the list that has already been sorted 
            if mylist[j] > current_value:#if the elements before theh element we are trying to insert is greater than our current value, we need to move it one position to the right to make space for our current value
                mylist[j + 1] = mylist[j]
                insert_index = j#This is to update the index where we will insert our current value
            else:
                break

        mylist[insert_index] = current_value # This is to insert the current value into the correct position in the sorted part of the list

    return mylist

def merge_sort(arr):
    mylist = arr.copy() #we make a copy so that the original list is not modified just like in insertion sort

    if len(mylist) > 1:#if the length of the list is greater than 1, we can proceed with the merge sort algorithm
        merge_sort_helper(mylist, 0, len(mylist) - 1)

    return mylist 


def merge_sort_helper(arr, left, right): #This is a helper function that will be used to recursively divide the list into smaller sublists until we reach the base case of a single element
    if left < right: # This is the base case for the recursion. If the left index is less than the right index, we can continue dividing the list.
        middle = left + (right - left) // 2 #This is to find the middle index of the list. We use this formula to avoid potential overflow issues that can occur with large lists.

        merge_sort_helper(arr, left, middle) #Then we recursively call the merge_sort_helper function on the left half of the list and the right half of the list. This is to continue dividing the list until we reach the base case of a single element.
        merge_sort_helper(arr, middle + 1, right)# Then we recursively call the merge_sort_helper function on the left half of the list and the right half of the list. This is to continue dividing the list until we reach the base case of a single element.

        merge(arr, left, middle, right) # And now we will merge the two halves of the list back together in sorted order. This is done by calling the merge function, which takes in the original list, the left index, the middle index, and the right index as arguments. The merge function will then combine the two halves of the list back together in sorted order.


def merge(arr, left, middle, right): #This is the merge function that will be used to combine the two halves of the list back together in sorted order. It takes in the original list, the left index, the middle index, and the right index as arguments.
    n1 = middle - left + 1 #This is the length of the left half of the list. We add 1 to account for the fact that the middle index is inclusive in the left half of the list.
    n2 = right - middle #This is the length of the right half of the list. We do not add 1 here because the middle index is exclusive in the right half of the list.

    L = [0] * n1 #This is to create a temporary list to hold the left half of the list. We initialize it with zeros and set its length to n1, which is the length of the left half of the list.
    R = [0] * n2# This is to create a temporary list to hold the right half of the list. We initialize it with zeros and set its length to n2, which is the length of the right half of the list.

    for i in range(n1):#We are iterating through the left half of the list and copying its elements into the temporary list L. This is done to ensure that we do not modify the original list while we are merging the two halves back together.
        L[i] = arr[left + i] # i is the index of the temporary list L, and left + i is the index of the original list arr. We add left to i to get the correct index in the original list for the left half of the list because the left index is inclusive in the left half of the list.

    for j in range(n2): #Same thing but for the right half of the list. We are iterating through the right half of the list and copying its elements into the temporary list R. This is done to ensure that we do not modify the original list while we are merging the two halves back together.
        R[j] = arr[middle + 1 + j]#we add 1 + j to the middle index to get the correct index in the original list for the right half of the list because the middle index is exclusive in the right half of the list.

    i = 0
    j = 0
    k = left #This is the index of the original list arr where we will start merging the two halves back together. We set it to left because we want to start merging the two halves back together at the left index of the original list.

    while i < n1 and j < n2: #We are comparng elements from the left half of the list and the right half of the list and merging them back together in sorted order. We continue this process until we have compared all elements from both halves of the list. The smaller element is placed in the original list arr at the index k, and we increment the index of the smaller element's temporary list (L or R) and the index k of the original list arr. This process continues until we have compared all elements from both halves of the list.
        if L[i] <= R[j]: #If the element in the left half of the list is less than or equal to the element in the right half of the list, we place the element from the left half of the list into the original list arr at the index k. We then increment the index i of the temporary list L and the index k of the original list arr.
            arr[k] = L[i]
            i += 1
        else: #else, if the element in the right half of the list is less than the element in the left half of the list, we place the element from the right half of the list into the original list arr at the index k. We then increment the index j of the temporary list R and the index k of the original list arr.
            arr[k] = R[j]
            j += 1

        k += 1

    while i < n1:# If there are any remaining elements in the left half of the list that have not been compared and merged back together, we place them into the original list arr at the index k. We then increment the index i of the temporary list L and the index k of the original list arr. This process continues until we have placed all remaining elements from the left half of the list into the original list arr.
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:# if there are any remaining elements in the right half of the list that have not been compared and merged back together, we place them into the original list arr at the index k. We then increment the index j of the temporary list R and the index k of the original list arr. This process continues until we have placed all remaining elements from the right half of the list into the original list arr.
        arr[k] = R[j]
        j += 1
        k += 1

def selection_sort(arr):
    arr = arr.copy() #this is to make a copy of the original list so that we do not modify it. This is important because we want to check that the original list is not modified by the sorting algorithm.
    #The way that selection sort works is that we iterate through the list and find the minimum element in the unsorted part of the list and swap it with the first element of the unsorted part of the list. We then repeat this process for the rest of the list until the entire list is sorted.
    for i in range(len(arr) - 1): #This loop is the loop that I mentioned beforehand which goes from the first element to the second to last element of the list. We do not need to go to the last element because by the time we get to the second to last element, the last element will already be in its correct position.
        min_index = i #This is the minimum index that we will use to keep track of the index of the minimum element in the unsorted part of the list. We initialize it to the current index i because we assume that the current element is the minimum element in the unsorted part of the list.

        for j in range(i + 1, len(arr)): #This inner loop actually goes through the unsorted part of the list and finds the minimum element in the unsorted part of the list. We start from i + 1 because we want to compare the current element with the rest of the elements in the unsorted part of the list.
            if arr[j] < arr[min_index]:#if the current element is less than the minimum element that we have found so far, we update the minimum index to the current index j.
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i] #and we swap the current element with the minimum element that we have found in the unsorted part of the list. This is done by using tuple unpacking to swap the elements at index i and min_index.

    return arr