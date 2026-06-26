import random
import csv 
import time
from sorting_algorithms import insertion_sort, merge_sort

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
        if n < 2:
            return data
        number_of_swaps = max(1, n // 20) #This is to ensure that we have at least one swap in the list. We divide n by 20 to get a number that is 5% of the size of the list. This will give us a good mix of sorted and unsorted values in the list. We use the max function to ensure that we have at least one swap in the list, even if n is less than 20. If n is less than 20, we will have a list with all sorted values, which is not what we want. By using max(1, n // 20), we ensure that we always have at least one swap in the list, regardless of the size of n.

        for _ in range(number_of_swaps):
            i = random.randint(0, n - 1)#This is to select a random index in the list. We use the random.randint function to generate a random integer between 0 and n - 1, which will give us a valid index in the list. This will ensure that we have a good mix of sorted and unsorted values in the list, and that they are randomly distributed throughout the list.
            j = random.randint(0, n - 1)
            data[i], data[j] = data[j], data[i] #This is to swap the values at the two randomly selected indices in the list. We use tuple unpacking to swap the values in a single line of code. This will ensure that we have a good mix of sorted and unsorted values in the list, and that they are randomly distributed throughout the list.

        return data
    elif data_type == "all_equal":
        return [1 for _ in range(n)] #It's literally all 1s.
    elif data_type == "few_unique":
        number_of_unique_values = max(2, int(n ** 0.5))#This line helps to make sure that we have at least 2 unique values in the list. We take the square root of n to get a number that is proportional to the size of the list. This will give us a good mix of unique and duplicate values in the list. We use the max function to ensure that we have at least 2 unique values in the list, even if n is less than 4. If n is less than 4, we will have a list with all duplicate values, which is not what we want. By using max(2, int(n ** 0.5)), we ensure that we always have at least 2 unique values in the list, regardless of the size of n.
        data = [random.randint(0, number_of_unique_values - 1) for _ in range(n)]#This is to create a list of length n with a mix of unique and duplicate values. We use the random.randint function to generate a random integer between 0 and number_of_unique_values - 1, which will give us a valid value for the list. This will ensure that we have a good mix of unique and duplicate values in the list, and that they are randomly distributed throughout the list.
        return data
    else:
        raise ValueError(f"Unknown data type: {data_type}")

def time_algorithm(sort_function, data, repeats):
    times = []

    for _ in range(repeats): #This is to run the sorting algorithm multiple times on the same data and take the average time. This will help to reduce the impact of any outliers or fluctuations in the timing results, and give us a more reliable measurement of the performance of the sorting algorithm for the given data type and size.
        start_time = time.perf_counter()
        sort_function(data)
        end_time = time.perf_counter()

        times.append(end_time - start_time)

    average_time = sum(times) / len(times) #and this is to take the averate time. 
    return average_time


def warm_up():#the reason I have this is because the first time a function is called, it can take longer due to various factors such as caching, memory allocation, and other optimizations that the Python interpreter may perform. By running the sorting algorithms on a small dataset before the actual benchmarking, we can ensure that these optimizations have already been performed and that the timing results are more accurate and consistent.
    data_types = ["random", "sorted", "reverse", "duplicates"]

    for data_type in data_types:
        sample_data = generate_data(100, data_type)

        insertion_sort(sample_data)
        merge_sort(sample_data)

def run_benchmarks():
    random.seed(300)#we need a seed because we want to be able to reproduce the results of the benchmark. If we do not set a seed, the random number generator will produce different results each time the benchmark is run, which will make it difficult to compare the results of different runs. By setting a seed, we ensure that the random number generator produces the same sequence of random numbers each time the benchmark is run, which allows us to compare the results of different runs more easily.
    RANDOM_SEED = 42
    MIN_SIZE = 0
    MAX_SIZE = 500
    SIZE_STEP = 1
    REPEATS = 10 #we can adjust these numbers later if needed.
    SIZES = list(range(MIN_SIZE, MAX_SIZE + 1, SIZE_STEP))#I wanted to use continous sizes from 0 to 500 with a step of 1. This will give us a good range of sizes to test the sorting algorithms on, and will allow us to see how the performance of the algorithms changes as the size of the input data increases. By using a step of 1, we can also see how the performance of the algorithms changes for small changes in the size of the input data, which can be useful for understanding the behavior of the algorithms in more detail.

    data_types = [
        "random",
        "sorted",
        "reverse",
        "duplicates",
        "nearly_sorted",
        "all_equal",
        "few_unique",
    ]

    warm_up()

    with open("results/benchmark_results.csv", "w", newline="") as file: #okay so this part is to open a file called benchmark_results.csv in the results directory for writing. The newline="" argument is used to ensure that the CSV file is written with the correct line endings, regardless of the operating system being used. This is important because different operating systems use different line endings (e.g., Windows uses \r\n, while Unix-based systems use \n), and using the wrong line endings can cause issues when reading the CSV file later. By specifying newline="", we ensure that the CSV file is written with the correct line endings for the current operating system.
        writer = csv.writer(file) #this is to create a CSV writer object that will be used to write data to the CSV file. The csv.writer function takes the file object as an argument and returns a writer object that can be used to write rows of data to the CSV file. We will use this writer object to write the benchmark results to the CSV file in a structured format, with each row representing a single benchmark result.

        writer.writerow([
            "data_type",
            "size",
            "algorithm",
            "average_time_seconds"
        ])

        for data_type in data_types: #This part is to iterate through each data type and size, generate the corresponding data, and time the sorting algorithms. The results are then written to the CSV file using the writer object. This allows us to systematically benchmark the sorting algorithms across different types of input data and sizes, and store the results in a structured format for later analysis.
            print(f"\nTesting data type: {data_type}")

            for size in SIZES:
                data = generate_data(size, data_type)

                insertion_time = time_algorithm(insertion_sort, data, REPEATS) #The REPEATS here is to ensure that we get a more accurate measurement of the time taken by the sorting algorithm. By running the sorting algorithm multiple times on the same data and taking the average time, we can reduce the impact of any outliers or fluctuations in the timing results. This will give us a more reliable measurement of the performance of the sorting algorithm for the given data type and size.
                merge_time = time_algorithm(merge_sort, data, REPEATS)

                writer.writerow([data_type, size, "insertion_sort", insertion_time])
                writer.writerow([data_type, size, "merge_sort", merge_time])

                print(
                    f"n={size:4d} | " #.4d means that the number will be printed with a width of 4 characters, and it will be right-aligned. If the number has fewer than 4 digits, it will be padded with spaces on the left to ensure that it takes up 4 characters in total. This formatting is useful for creating a clean and aligned output when printing multiple numbers in a table-like format.
                    f"insertion={insertion_time:.8f}s | "#.8f means that the number will be printed as a floating-point number with 8 digits after the decimal point. This formatting is useful for displaying timing results with a high level of precision, allowing us to see small differences in the performance of the sorting algorithms. The 's' at the end indicates that the time is measured in seconds.
                    f"merge={merge_time:.8f}s"#and f in general is used to indicate that the string is a formatted string literal, which allows us to embed expressions inside the string using curly braces {}. The expressions are evaluated at runtime, and their values are inserted into the string at the corresponding positions. This makes it easy to create dynamic strings that include variable values or computed results, such as the timing results of the sorting algorithms in this case.
                )

    print("\nBenchmarking finished. Results saved to results/benchmark_results.csv")


if __name__ == "__main__":
    run_benchmarks()

"""
if __name__ == "__main__":
    sizes = [5, 10, 20,50,100]
    data_types = [
    "random",
    "sorted",
    "reverse",
    "duplicates",
    "nearly_sorted",
    "all_equal",
    "few_unique"
]

    for data_type in data_types:
        print(f"\nData type: {data_type}")

        for n in sizes:
            data = generate_data(n, data_type)
            print(f"n = {n}: {data}")



"""
