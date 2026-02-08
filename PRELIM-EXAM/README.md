# Sorting Algorithm Stress Test

**PRELIM EXAM - Design and Analysis of Algorithms LAB**

A GUI-based benchmarking tool for testing sorting algorithm performance on large CSV datasets.

---

## Project Structure

```
sorting-algorithm-stress-test/
│
├── data/
│   └── generated_data.csv          # 100,000 records dataset
│
└── src/
    ├── sorting_algorithms.py       # Sorting implementations
    └── main.py                     # GUI application
```

---

## Algorithms Implemented

| Algorithm | Time Complexity (Best) | Time Complexity (Average) | Time Complexity (Worst) | Space Complexity |
|-----------|----------------------|--------------------------|------------------------|------------------|
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) |
| **Bubble Sort** | O(n) | O(n²) | O(n²) | O(1) |
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) |

---

## How to Run

1. Navigate to the `src` directory:
   ```bash
   cd src
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Use the GUI to:
   - Select sorting algorithm
   - Choose column to sort by (ID, FirstName, LastName)
   - Enter dataset size or use quick-select buttons
   - Click START BENCHMARK

---

## Features

- **Column Selection**: Sort by ID (integer), FirstName (string), or LastName (string)
- **Scalable Testing**: Test with datasets from 1 to 100,000 records
- **Performance Tracking**: Displays execution time and records processed
- **Progress Bar**: Real-time progress updates
- **Warning System**: Alerts for O(n²) algorithms on large datasets (>15,000 records)
- **Results Display**: Shows top 100 sorted records
- **Cancellation**: Stop long-running operations with STOP button

---

## Benchmark Results

### Performance Testing Results

#### 1,000 Records

| Algorithm | Execution Time |
|-----------|----------------|
| Merge Sort | 0.3214 seconds |
| Bubble Sort | 0.3731 seconds |
| Insertion Sort | 0.0732 seconds |

#### 10,000 Records

| Algorithm | Execution Time |
|-----------|----------------|
| Merge Sort | 2.9247 seconds |
| Bubble Sort | 15.9879 seconds |
| Insertion Sort | 4.6867 seconds |

#### 100,000 Records

| Algorithm | Execution Time |
|-----------|----------------|
| Merge Sort | 31.4792 seconds |
| Bubble Sort | 33.3 minutes |
| Insertion Sort | 11.1 minutes |

---

## Observations

- **Merge Sort**: Maintains consistent O(n log n) performance across all dataset sizes. Completes 100,000 records in under a minute.

- **Insertion Sort & Bubble Sort**: Acceptable performance on small datasets (N ≤ 1,000), but execution time grows quadratically. At N = 100,000, these algorithms become impractical (taking several minutes to hours).

- **Recommendation**: Use Merge Sort for datasets larger than 10,000 records.

---

## Requirements

- Python 3.7+
- Tkinter (included with Python)

---

## Notes

- All sorting algorithms implemented from scratch (no built-in `.sort()` functions used)
- Progress tracking included for long-running operations
- Dataset must be in `data/generated_data.csv` format with columns: ID, FirstName, LastName
