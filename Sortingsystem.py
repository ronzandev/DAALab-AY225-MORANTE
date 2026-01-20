import time
import os

def bubble_sort_descending(arr):
    """
    Sorts an array in DESCENDING order using the bubble sort algorithm.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    n = len(arr)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        if not swapped:
            break
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    return arr, time_taken


def insertion_sort_descending(arr):
    """
    Sorts an array in DESCENDING order using the insertion sort algorithm.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    return arr, time_taken


def merge_sort_descending(arr):
    """
    Sorts an array in DESCENDING order using the merge sort algorithm.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    
    def merge_sort_helper(arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = merge_sort_helper(arr[:mid])
        right = merge_sort_helper(arr[mid:])
        
        return merge(left, right)
    
    def merge(left, right):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] >= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    sorted_arr = merge_sort_helper(arr)
    end_time = time.time()
    time_taken = end_time - start_time
    
    return sorted_arr, time_taken


def read_dataset(filename):
    """
    Reads numbers from a file and returns them as a list.
    Each number should be on a separate line or separated by spaces/commas.
    
    Args:
        filename: Path to the file containing numbers
        
    Returns:
        List of numbers read from the file
    """
    try:
        with open(filename, 'r') as file:
            numbers = []
            for line in file:
                line = line.strip()
                if line:
                    try:
                        if '.' in line:
                            numbers.append(float(line))
                        else:
                            numbers.append(int(line))
                    except ValueError:
                        if ',' in line:
                            nums = [float(x.strip()) if '.' in x.strip() else int(x.strip()) 
                                   for x in line.split(',') if x.strip()]
                            numbers.extend(nums)
                        else:
                            nums = [float(x.strip()) if '.' in x.strip() else int(x.strip()) 
                                   for x in line.split() if x.strip()]
                            numbers.extend(nums)
            
            return numbers
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def display_menu():
    """
    Displays the main menu.
    """
    print("\n==========================================")
    print("      SORTING ALGORITHMS MENU")
    print("==========================================")
    print("1. Bubble Sort")
    print("2. Insertion Sort")
    print("3. Merge Sort")
    print("4. Compare All Sorting Times")
    print("5. Exit")
    print("==========================================")


def display_sorted_results(sorted_data, time_taken, algorithm_name):
    """
    Displays the sorted data and statistics.
    """
    print("\nSORTING COMPLETE!\n")
    print("Sorted elements (descending order):\n")
    
    for num in sorted_data:
        print(f"{num}")
    
    print(f"\n==========================================")
    print(f"Algorithm: {algorithm_name}")
    print(f"Time taken: {time_taken:.6f} seconds")
    print(f"Total elements sorted: {len(sorted_data)}")
    
    is_sorted = all(sorted_data[i] >= sorted_data[i+1] for i in range(len(sorted_data)-1))
    print(f"Verification: {'✓ CORRECT!' if is_sorted else '✗ FAILED!'}")
    print("==========================================")


def compare_all_sorts(data):
    """
    Compares the performance of all three sorting algorithms.
    """
    print("\n==========================================")
    print("   COMPARING ALL SORTING ALGORITHMS")
    print("==========================================\n")
    
    print("Running Bubble Sort...")
    _, bubble_time = bubble_sort_descending(data.copy())
    print(f"✓ Bubble Sort completed in {bubble_time:.6f} seconds")
    
    print("\nRunning Insertion Sort...")
    _, insertion_time = insertion_sort_descending(data.copy())
    print(f"✓ Insertion Sort completed in {insertion_time:.6f} seconds")
    
    print("\nRunning Merge Sort...")
    _, merge_time = merge_sort_descending(data.copy())
    print(f"✓ Merge Sort completed in {merge_time:.6f} seconds")
    
    print("\n==========================================")
    print("           COMPARISON RESULTS")
    print("==========================================")
    print(f"Bubble Sort:    {bubble_time:.6f} seconds")
    print(f"Insertion Sort: {insertion_time:.6f} seconds")
    print(f"Merge Sort:     {merge_time:.6f} seconds")
    print("==========================================")
    
    # Determine the fastest
    times = {
        'Bubble Sort': bubble_time,
        'Insertion Sort': insertion_time,
        'Merge Sort': merge_time
    }
    fastest = min(times, key=times.get)
    print(f"\n🏆 FASTEST: {fastest} ({times[fastest]:.6f} seconds)")
    print("==========================================")


# Main program
if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to dataset.txt in the same directory
    filename = os.path.join(script_dir, "dataset.txt")
    
    print(f"Reading data from '{filename}'...")
    
    data = read_dataset(filename)
    
    if data is None:
        print("Failed to read data. Exiting program.")
        exit()
    
    print(f"Dataset loaded: {len(data)} elements")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\n>>> Running BUBBLE SORT...")
            sorted_data, time_taken = bubble_sort_descending(data.copy())
            display_sorted_results(sorted_data, time_taken, "BUBBLE SORT")
            
        elif choice == '2':
            print("\n>>> Running INSERTION SORT...")
            sorted_data, time_taken = insertion_sort_descending(data.copy())
            display_sorted_results(sorted_data, time_taken, "INSERTION SORT")
            
        elif choice == '3':
            print("\n>>> Running MERGE SORT...")
            sorted_data, time_taken = merge_sort_descending(data.copy())
            display_sorted_results(sorted_data, time_taken, "MERGE SORT")
            
        elif choice == '4':
            compare_all_sorts(data)
            
        elif choice == '5':
            print("\n<=========================================>")
            print("   Goodbye! Thanks for stopping by :)    ")
            print("<==========================================>\n")
            break
            
        else:
            print("\n⚠ Invalid choice! Please enter a number between 1 and 5.")