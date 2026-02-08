"""
Sorting Algorithms - DAA Prelim Exam
Bubble Sort, Insertion Sort, Merge Sort
"""

import math

def bubble_sort(data, key, descending=False, progress_callback=None, cancel_event=None):
    """
    Bubble Sort - compares neighbors and swaps them
    O(n²) time, O(1) space
    """
    # Make a copy so we don't mess up the original list
    data = data[:]
    n = len(data)
    
    # Setup cancel checker (for the STOP button)
    is_cancelled = cancel_event.is_set if cancel_event else (lambda: False)
    
    # Figure out how many comparisons we'll do total
    total_comparisons = n * (n - 1) // 2
    comparisons_done = 0
    
    # Go through the list multiple times
    for i in range(n):
        # Check if user pressed STOP
        if is_cancelled():
            return None
            
        swapped = False
        comparisons_in_pass = n - i - 1
        
        # Compare each pair of neighbors
        for j in range(0, comparisons_in_pass):
            val1 = data[j].get(key)
            val2 = data[j+1].get(key)
            
            # Figure out if we need to swap these two
            should_swap = False
            if descending:
                if val1 < val2:
                    should_swap = True
            else:
                if val1 > val2:
                    should_swap = True
                    
            if should_swap:
                # Swap the two items
                data[j], data[j+1] = data[j+1], data[j]
                swapped = True
            
            # Every 1000 comparisons, check if user wants to stop
            if j % 1000 == 0 and is_cancelled():
                return None
        
        # Update the progress bar
        comparisons_done += comparisons_in_pass
        if progress_callback:
            p = (comparisons_done / total_comparisons) * 100
            progress_callback(min(p, 99.9))
        
        # If nothing got swapped this round, we're done early!
        if not swapped:
            break
    
    # Set progress to 100%
    if progress_callback:
        progress_callback(100)
    return data

def insertion_sort(data, key, descending=False, progress_callback=None, cancel_event=None):
    """
    Insertion Sort - picks elements and puts them in the right spot
    O(n²) time, O(1) space
    """
    # Make a copy so we don't mess up the original list
    data = data[:]
    n = len(data)
    
    # Setup cancel checker
    is_cancelled = cancel_event.is_set if cancel_event else (lambda: False)
    
    # Start from second item (first item is already "sorted")
    for i in range(1, n):
        # Check if user pressed STOP
        if is_cancelled():
            return None
            
        # Grab the current item we're trying to place
        current_record = data[i]
        current_val = current_record.get(key)
        j = i - 1
        
        # Move backwards through the sorted part
        while j >= 0:
            compare_val = data[j].get(key)
            should_move = False
            
            # Check if we need to keep moving
            if descending:
                if compare_val < current_val:
                    should_move = True
            else:
                if compare_val > current_val:
                    should_move = True
            
            if should_move:
                # Scoot this item to the right to make room
                data[j + 1] = data[j]
                j -= 1
            else:
                # Found the right spot!
                break
        
        # Drop the current item into its correct position
        data[j + 1] = current_record
        
        # Update progress bar every 10 items
        if progress_callback and i % 10 == 0:
            p = (i / n) ** 2 * 100
            progress_callback(p)
    
    # Set progress to 100%
    if progress_callback:
        progress_callback(100)
    return data

def merge_sort(data, key, descending=False, progress_callback=None, cancel_event=None):
    """
    Merge Sort - splits array in half, sorts each half, then combines
    O(n log n) time, O(n) space
    """
    # Base case: list with 0 or 1 item is already sorted
    if len(data) <= 1:
        return data
    
    # Setup cancel checker
    is_cancelled = cancel_event.is_set if cancel_event else (lambda: False)
    
    # Calculate total work for progress tracking
    total_elements = len(data)
    total_work = total_elements * math.log2(total_elements) if total_elements > 1 else 1
    state = [0]  # Using a list so the inner function can modify it
    
    def merge_recursive(arr):
        # Check if user pressed STOP
        if is_cancelled():
            return None
            
        # Base case: tiny lists don't need sorting
        if len(arr) <= 1:
            return arr
            
        # Split the list in half
        mid = len(arr) // 2
        left_half = merge_recursive(arr[:mid])
        if left_half is None:
            return None
            
        right_half = merge_recursive(arr[mid:])
        if right_half is None:
            return None
        
        # Now merge the two sorted halves back together
        merged = []
        i = j = 0
        
        # Pick the smaller item from left or right until one runs out
        while i < len(left_half) and j < len(right_half):
            if is_cancelled():
                return None
                
            val1 = left_half[i].get(key)
            val2 = right_half[j].get(key)
            
            # Decide which side to pick from
            pick_left = False
            if descending:
                if val1 >= val2:
                    pick_left = True
            else:
                if val1 <= val2:
                    pick_left = True
            
            if pick_left:
                merged.append(left_half[i])
                i += 1
            else:
                merged.append(right_half[j])
                j += 1
        
        # Add any leftover items
        merged.extend(left_half[i:])
        merged.extend(right_half[j:])
        
        # Update progress bar
        state[0] += len(arr)
        if progress_callback:
            p = (state[0] / total_work) * 100
            progress_callback(min(p, 99.9))
        
        return merged
    
    # Start the recursive sorting
    result = merge_recursive(data[:])
    if result is None:
        return None
        
    # Set progress to 100%
    if progress_callback:
        progress_callback(100)
    return result
