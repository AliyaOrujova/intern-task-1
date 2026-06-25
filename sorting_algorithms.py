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