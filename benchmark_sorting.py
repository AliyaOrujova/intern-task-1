import random


def generate_data(n, data_type):
    if data_type == "random":
        return [random.randint(0, n * 10) for _ in range(n)] #random numbers should come from a range that is larger than the size of the list to ensure that we have a good mix of numbers. We multiply n by 10 to get a range that is 10 times larger than the size of the list. This will give us a good mix of numbers and will help us test the sorting algorithms more effectively. I used _ instead of i because the variable is not actually used in the list comprehension. This is a common convention in Python to indicate that the variable is not used. It helps to make the code more readable and indicates that the variable is not important for the logic of the code.

    elif data_type == "sorted":
        return list(range(n)) #This just makes an already sorted list of length n with consecutive numbers starting from 0. 

    elif data_type == "reverse":
        return list(range(n, 0, -1)) #This just makes a reverse sorted list of length n with consecutive numbers starting from n and going down to 1. The range function is used to generate a sequence of numbers, and the step parameter is set to -1 to generate the numbers in reverse order. The list function is then used to convert the range object into a list. The zero is not included in the list because the range function generates numbers up to, but not including, the stop value. In this case, the stop value is 0, so the list will contain numbers from n down to 1.

    elif data_type == "duplicates":
        number_of_unique_values = max(1, n // 10) #This is to ensure that we have at least one unique value in the list. We divide n by 10 to get a number that is 10% of the size of the list. This will give us a good mix of unique and duplicate values in the list. We use the max function to ensure that we have at least one unique value in the list, even if n is less than 10. If n is less than 10, we will have a list with all duplicate values, which is not what we want. By using max(1, n // 10), we ensure that we always have at least one unique value in the list, regardless of the size of n.
        data = [i % number_of_unique_values for i in range(n)] #This is to create a list of length n with a mix of unique and duplicate values. We use the modulo operator to ensure that we have a good mix of unique and duplicate values in the list. The modulo operator returns the remainder of the division of i by number_of_unique_values, which will give us a value between 0 and number_of_unique_values - 1. This will ensure that we have a good mix of unique and duplicate values in the list. For example, if n is 20 and number_of_unique_values is 2, we will have a list with 10 unique values (0 and 1) and 10 duplicate values (0 and 1). 
        random.shuffle(data) #This is to shuffle the list so that the unique and duplicate values are randomly distributed throughout the list. We use the random.shuffle function to shuffle the list in place, which means that the original list is modified and the elements are randomly rearranged. This will ensure that we have a good mix of unique and duplicate values in the list, and that they are randomly distributed throughout the list.
        return data
    elif data_type == "nearly_sorted":
        data = list(range(n))
        number_of_swaps = max(1, n // 20) #This is to ensure that we have at least one swap in the list. We divide n by 20 to get a number that is 5% of the size of the list. This will give us a good mix of sorted and unsorted values in the list. We use the max function to ensure that we have at least one swap in the list, even if n is less than 20. If n is less than 20, we will have a list with all sorted values, which is not what we want. By using max(1, n // 20), we ensure that we always have at least one swap in the list, regardless of the size of n.

        for _ in range(number_of_swaps):
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            data[i], data[j] = data[j], data[i]

        return data
    elif data_type == "all_equal":
        return [1 for _ in range(n)]
    elif data_type == "few_unique":
        number_of_unique_values = max(2, int(n ** 0.5))
        data = [random.randint(0, number_of_unique_values - 1) for _ in range(n)]
        return data
    else:
        raise ValueError(f"Unknown data type: {data_type}")
    

if __name__ == "__main__":
    sizes = [5, 10, 20]
    data_types = [
    "random",
    "sorted",
    "reverse",
    "duplicates",
    "nearly_sorted",
    "all_equal"
]

    for data_type in data_types:
        print(f"\nData type: {data_type}")

        for n in sizes:
            data = generate_data(n, data_type)
            print(f"n = {n}: {data}")