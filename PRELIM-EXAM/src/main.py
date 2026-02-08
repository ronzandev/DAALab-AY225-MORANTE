import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import os
import csv
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import sorting_algorithms

DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'generated_data.csv')

class SortingBenchmarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("The Sorting Algorithm Stress Test")
        self.geometry("1600x900")
        self.minsize(1600, 900)
        
        self.colors = {
            'bg': '#F4F0FA',
            'sidebar': '#E6DDF5',
            'card': '#FFFFFF',
            'primary': '#9B7EBD',
            'secondary': '#B8A4D4',
            'accent': '#7C5FA3',
            'text_dark': '#3D2C5C',
            'text_light': '#6B5B7A',
            'border': '#D4C5E8',
            'success': '#8BC34A',
            'warning': '#FF9800',
            'danger': '#E57373'
        }
        
        self.configure(bg=self.colors['bg'])
        
        self.dataset = []
        self.sorted_result = []
        self.is_data_ready = False
        self.stop_signal = threading.Event()
        
        self.selected_algorithm = tk.StringVar(value="Merge Sort")
        self.selected_column = tk.StringVar(value="ID")
        self.dataset_size = tk.StringVar(value="5000")
        
        # Animation control
        self.animation_running = False
        self.animation_frame = 0
        
        self._build_interface()
        self._load_dataset_async()
        
    def _build_interface(self):
        main_container = tk.Frame(self, bg=self.colors['bg'])
        main_container.pack(fill="both", expand=True)
        
        left_panel = self._create_control_panel(main_container)
        left_panel.pack(side="left", fill="y", padx=(0, 1))
        
        right_panel = self._create_content_panel(main_container)
        right_panel.pack(side="right", fill="both", expand=True)
        
    def _create_control_panel(self, parent):
        panel = tk.Frame(parent, bg=self.colors['sidebar'], width=320)
        panel.pack_propagate(False)
        
        tk.Label(
            panel, text="PRELIM EXAM\nDAA-LAB",
            font=("Helvetica", 20, "bold"),
            bg=self.colors['sidebar'],
            fg=self.colors['text_dark'],
            justify="center"
        ).pack(pady=(40, 30))
        
        config_section = tk.Frame(panel, bg=self.colors['card'], padx=20, pady=20)
        config_section.pack(fill="x", padx=20, pady=(0, 15))
        
        tk.Label(
            config_section, text="Algorithm Selection",
            font=("Arial", 10, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text_dark']
        ).pack(anchor="w", pady=(0, 8))
        
        algorithms = ["Merge Sort", "Bubble Sort", "Insertion Sort"]
        for algo in algorithms:
            rb = tk.Radiobutton(
                config_section,
                text=algo,
                variable=self.selected_algorithm,
                value=algo,
                font=("Arial", 10),
                bg=self.colors['card'],
                fg=self.colors['text_light'],
                selectcolor=self.colors['secondary'],
                activebackground=self.colors['card'],
                cursor="hand2"
            )
            rb.pack(anchor="w", pady=2)
        
        tk.Label(
            config_section, text="Sort Column By",
            font=("Arial", 10, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text_dark']
        ).pack(anchor="w", pady=(15, 8))
        
        column_combo = ttk.Combobox(
            config_section,
            textvariable=self.selected_column,
            values=["ID", "FirstName", "LastName"],
            state="readonly",
            font=("Arial", 10)
        )
        column_combo.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            config_section, text="Number of Records (Dataset Size)",
            font=("Arial", 10, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text_dark']
        ).pack(anchor="w", pady=(0, 8))
        
        size_entry = tk.Entry(
            config_section,
            textvariable=self.dataset_size,
            font=("Arial", 11),
            bg="#FAFAFA",
            fg=self.colors['text_dark'],
            relief="solid",
            bd=1
        )
        size_entry.pack(fill="x", ipady=8)
        
        self.size_hint = tk.Label(
            config_section, text="Loading data...",
            font=("Arial", 8),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        )
        self.size_hint.pack(anchor="w", pady=(4, 0))
        
        quick_select = tk.Frame(config_section, bg=self.colors['card'])
        quick_select.pack(fill="x", pady=(10, 0))
        
        for label, value in [("1K", "1000"), ("10K", "10000"), ("50K", "50000"), ("MAX", "MAX")]:
            tk.Button(
                quick_select, text=label,
                font=("Arial", 8, "bold"),
                bg=self.colors['secondary'],
                fg="white",
                bd=0,
                padx=10,
                pady=4,
                cursor="hand2",
                command=lambda v=value: self.dataset_size.set(v)
            ).pack(side="left", padx=3)
        
        button_frame = tk.Frame(panel, bg=self.colors['sidebar'])
        button_frame.pack(pady=30)
        
        self.run_btn = tk.Button(
            button_frame, text="START BENCHMARK",
            font=("Arial", 12, "bold"),
            bg=self.colors['primary'],
            fg="white",
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2",
            command=self._execute_benchmark
        )
        self.run_btn.pack(pady=(0, 10))
        
        self.stop_btn = tk.Button(
            button_frame, text="STOP",
            font=("Arial", 11, "bold"),
            bg=self.colors['danger'],
            fg="white",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            state="disabled",
            command=self._cancel_benchmark
        )
        self.stop_btn.pack()
        
        return panel
        
    def _create_content_panel(self, parent):
        # Create a canvas with scrollbar for the content panel
        canvas = tk.Canvas(parent, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        
        # Frame that will contain all the scrollable content
        panel = tk.Frame(canvas, bg=self.colors['bg'])
        
        # Configure canvas scrolling
        panel.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Create window with full width - store the window id
        canvas_window = canvas.create_window((0, 0), window=panel, anchor="nw")
        
        # Bind canvas width changes to update the panel width
        def _configure_panel_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _configure_panel_width)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        header = tk.Frame(panel, bg=self.colors['bg'])
        header.pack(fill="x", padx=40, pady=(40, 20))
        
        self.title_label = tk.Label(
            header, text="The Sorting Algorithm Stress Test",
            font=("Helvetica", 26, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text_dark']
        )
        self.title_label.pack(anchor="w")
        
        self.subtitle_label = tk.Label(
            header, text="Awaiting benchmark execution",
            font=("Arial", 11),
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        )
        self.subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Metrics row - responsive layout with 2 cards
        metrics_row = tk.Frame(panel, bg=self.colors['bg'])
        metrics_row.pack(fill="x", padx=40, pady=(0, 25))
        
        # Allow grid to control the size
        metrics_row.grid_propagate(True)
        
        # Configure grid columns to expand equally (2 columns only)
        metrics_row.grid_columnconfigure(0, weight=1)
        metrics_row.grid_columnconfigure(1, weight=1)
        
        self.time_metric = self._create_metric_card(metrics_row, "Execution Time", "--", "seconds")
        self.time_metric.grid(row=0, column=0, sticky="ew", padx=(0, 15))
        
        self.records_metric = self._create_metric_card(metrics_row, "Records Processed", "--", "records")
        self.records_metric.grid(row=0, column=1, sticky="ew")
        
        progress_section = tk.Frame(panel, bg=self.colors['card'], padx=20, pady=15)
        progress_section.pack(fill="x", padx=40, pady=(0, 20))
        
        # Progress header with animated emoticon
        progress_header = tk.Frame(progress_section, bg=self.colors['card'])
        progress_header.pack(anchor="w", pady=(0, 8))
        
        tk.Label(
            progress_header, text="Progress Bar... ",
            font=("Arial", 10, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text_dark']
        ).pack(side="left")
        
        # Animated emoticon label
        self.progress_emoticon = tk.Label(
            progress_header, text="",
            font=("Arial", 10),
            bg=self.colors['card'],
            fg=self.colors['text_dark']
        )
        self.progress_emoticon.pack(side="left")
        
        self.progress_bar = ttk.Progressbar(
            progress_section,
            mode="determinate",
            length=300
        )
        self.progress_bar.pack(fill="x")

        results_section = tk.Frame(panel, bg=self.colors['card'], padx=20, pady=20)
        results_section.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        tk.Label(
            results_section, text="First 100 Sorted Datasets",
            font=("Arial", 11, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text_dark']
        ).pack(anchor="w", pady=(0, 10))
        
        tree_frame = tk.Frame(results_section, bg=self.colors['card'])
        tree_frame.pack(fill="both", expand=True)
        
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        
        self.results_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "FirstName", "LastName"),
            show="headings",
            yscrollcommand=tree_scroll.set,
            height=15
        )
        
        self.results_tree.heading("ID", text="ID")
        self.results_tree.heading("FirstName", text="First Name")
        self.results_tree.heading("LastName", text="Last Name")
        
        self.results_tree.column("ID", width=120, anchor="w")
        self.results_tree.column("FirstName", width=200, anchor="w")
        self.results_tree.column("LastName", width=200, anchor="w")
        
        self.results_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.config(command=self.results_tree.yview)
        
        # Dataset Preview section at the bottom (same width as other sections)
        preview_section = tk.Frame(panel, bg=self.colors['card'], padx=20, pady=15)
        preview_section.pack(fill="x", padx=40, pady=(0, 40))
        
        tk.Label(
            preview_section, text="Dataset Preview (First 50 Records)",
            font=("Arial", 10, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text_dark']
        ).pack(anchor="w", pady=(0, 8))
        
        self.preview_text = tk.Text(
            preview_section,
            font=("Consolas", 9),
            bg="#FAFAFA",
            fg=self.colors['text_light'],
            height=8,
            bd=0,
            state="disabled"
        )
        self.preview_text.pack(fill="x")

        return canvas  # Return canvas instead of panel
        
    def _create_metric_card(self, parent, title, value, unit):
        card = tk.Frame(parent, bg=self.colors['card'], height=130)
        # Don't use pack_propagate(False) - let the card expand with grid
        
        tk.Label(
            card, text=title,
            font=("Arial", 9),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack(pady=(15, 5))
        
        value_label = tk.Label(
            card, text=value,
            font=("Helvetica", 24, "bold"),
            bg=self.colors['card'],
            fg=self.colors['primary']
        )
        value_label.pack()
        
        unit_label = tk.Label(
            card, text=unit,
            font=("Arial", 9),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        )
        unit_label.pack()
        
        card.value_label = value_label
        card.unit_label = unit_label
        
        return card
        
    def _update_metric(self, card, value, unit=None):
        card.value_label.config(text=str(value))
        if unit is not None:
            card.unit_label.config(text=unit)
    
    def _animate_progress_emoticon(self):
        """Animate the emoticon next to the progress bar"""
        if not self.animation_running:
            return
        
        # Cycle through different cat emoticons
        emoticons = ["/ᐠ - ˕ -マ", "/ᐠ｡ꞈ｡ᐟ\\", "/ᐠ. ᴗ.ᐟ\\", "/ᐠ - ˕ -マ ᶻ 𝗓 𐰁"]
        
        self.progress_emoticon.config(text=emoticons[self.animation_frame])
        self.animation_frame = (self.animation_frame + 1) % len(emoticons)
        
        # Schedule next frame (update every 500ms)
        self.after(500, self._animate_progress_emoticon)
    
    def _start_animation(self):
        """Start the progress bar emoticon animation"""
        self.animation_running = True
        self.animation_frame = 0
        self._animate_progress_emoticon()
    
    def _stop_animation(self):
        """Stop the progress bar emoticon animation"""
        self.animation_running = False
        self.progress_emoticon.config(text="")
            
    def _load_dataset_async(self):
        threading.Thread(target=self._load_dataset, daemon=True).start()
        
    def _load_dataset(self):
        try:
            start_time = time.perf_counter()
            
            with open(DATA_FILE_PATH, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        row['ID'] = int(row['ID'])
                    except (ValueError, KeyError):
                        pass
                    self.dataset.append(row)
            
            load_duration = time.perf_counter() - start_time
            self.is_data_ready = True
            
            self.after(0, lambda: self._update_status(
                f"Dataset loaded: {len(self.dataset):,} items was loaded in approximately {load_duration:.2f}s | ദ്ദി(ᵔᗜᵔ)"
            ))
            self.after(0, lambda: self.size_hint.config(
                text=f"Available: 1 to {len(self.dataset):,}"
            ))
            self.after(0, self._display_preview)
            
        except Exception as e:
            self.after(0, lambda: self._update_status(f"Error: {str(e)}"))
            
    def _display_preview(self):
        if not self.dataset:
            return
            
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", "end")
        
        lines = []
        lines.append(f"{'ID':<10} {'FirstName':<20} {'LastName':<20}")
        lines.append("-" * 50)
        
        # Display first 50 records
        for record in self.dataset[:50]:
            lines.append(
                f"{str(record.get('ID', 'N/A')):<10} "
                f"{record.get('FirstName', 'N/A'):<20} "
                f"{record.get('LastName', 'N/A'):<20}"
            )
        
        self.preview_text.insert("1.0", "\n".join(lines))
        self.preview_text.config(state="disabled")
        
    def _update_status(self, message):
        self.subtitle_label.config(text=message)
        
    def _update_progress(self, value):
        self.after(0, lambda: self.progress_bar.config(value=value))
        
    def _execute_benchmark(self):
        if not self.is_data_ready:
            messagebox.showerror("Error", "Dataset not loaded (ㆆ_ㆆ)")
            return
            
        size_input = self.dataset_size.get().strip()
        
        if size_input.upper() == "MAX":
            n = len(self.dataset)
        else:
            try:
                n = int(size_input)
                if n <= 0 or n > len(self.dataset):
                    messagebox.showerror(
                        "Invalid Input (ㆆ_ㆆ)",
                        f"Enter a number between 1 and {len(self.dataset):,}"
                    )
                    return
            except ValueError:
                messagebox.showerror("Invalid Input", "Enter a valid number or 'MAX' (ㆆ_ㆆ)")
                return
        
        algorithm = self.selected_algorithm.get()
        column = self.selected_column.get()
        
        if n > 15000 and algorithm in ["Bubble Sort", "Insertion Sort"]:
            if not self._show_warning(algorithm, n):
                return
        
        self.stop_signal.clear()
        self.progress_bar['value'] = 0
        
        self.run_btn.config(state="disabled", text="RUNNING...")
        self.stop_btn.config(state="normal")
        
        # Start the animation
        self._start_animation()
        
        self._update_status("Executing benchmark... /ᐠ - ˕ -マ ᶻ 𝗓 𐰁")
        self.title_label.config(text="Benchmark In Progress")
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        threading.Thread(
            target=self._run_sort,
            args=(n, algorithm, column),
            daemon=True
        ).start()
        
    def _cancel_benchmark(self):
        self.stop_signal.set()
        self._update_status("Cancelling... /ᐠ - ˕ -マ ᶻ 𝗓 𐰁")
        
    def _run_sort(self, n, algorithm, column):
        subset = list(self.dataset[:n])
        
        start = time.perf_counter()
        result = None
        
        try:
            if algorithm == "Bubble Sort":
                result = sorting_algorithms.bubble_sort(
                    subset, column,
                    progress_callback=self._update_progress,
                    cancel_event=self.stop_signal
                )
            elif algorithm == "Insertion Sort":
                result = sorting_algorithms.insertion_sort(
                    subset, column,
                    progress_callback=self._update_progress,
                    cancel_event=self.stop_signal
                )
            elif algorithm == "Merge Sort":
                result = sorting_algorithms.merge_sort(
                    subset, column,
                    progress_callback=self._update_progress,
                    cancel_event=self.stop_signal
                )
        except Exception as e:
            self.after(0, lambda: self._handle_error(str(e)))
            return
        
        duration = time.perf_counter() - start
        
        if result is None:
            self.after(0, self._handle_cancellation)
        else:
            self.sorted_result = result
            self.after(0, lambda: self._display_results(result, duration, n, algorithm, column))
            
    def _display_results(self, data, duration, n, algorithm, column):
        # Stop the animation
        self._stop_animation()
        
        self.run_btn.config(state="normal", text="START BENCHMARK")
        self.stop_btn.config(state="disabled")
        
        self.title_label.config(text="Benchmark Complete")
        self._update_status(f"Sorted {n:,} records by {column} using {algorithm} ദ്ദി(ᵔᗜᵔ)")
        
        self.progress_bar['value'] = 100
        
        self._update_metric(self.time_metric, f"{duration:.4f}", "seconds")
        self._update_metric(self.records_metric, f"{n:,}", "records")
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        for i, record in enumerate(data[:100]):
            tag = "even" if i % 2 == 0 else "odd"
            self.results_tree.insert("", "end", values=(
                record.get('ID', 'N/A'),
                record.get('FirstName', 'N/A'),
                record.get('LastName', 'N/A')
            ), tags=(tag,))
        
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, background=self.colors['card'], foreground=self.colors['text_dark'])
        self.results_tree.tag_configure("even", background="#FFFFFF")
        self.results_tree.tag_configure("odd", background="#F9F7FC")
        
    def _handle_cancellation(self):
        # Stop the animation
        self._stop_animation()
        
        self.run_btn.config(state="normal", text="START BENCHMARK")
        self.stop_btn.config(state="disabled")
        
        self.title_label.config(text="Benchmark Cancelled")
        self._update_status("Operation cancelled by user (╭ರ_•́)?")
        
        self.progress_bar['value'] = 0
        
        self._update_metric(self.time_metric, "--", "seconds")
        self._update_metric(self.records_metric, "--", "records")
        
    def _handle_error(self, error_msg):
        # Stop the animation
        self._stop_animation()
        
        self.run_btn.config(state="normal", text="START BENCHMARK")
        self.stop_btn.config(state="disabled")
        
        self.title_label.config(text="Error Occurred")
        self._update_status(f"Error: {error_msg}")
        
        messagebox.showerror("Benchmark Error (ㆆ_ㆆ)", error_msg)
        
    def _show_warning(self, algorithm, n):
        import math
        
        if algorithm == "Bubble Sort":
            ops = n * n
            ops_per_sec = 5000000
        else:
            ops = (n * n) / 2
            ops_per_sec = 7500000
        
        seconds = ops / ops_per_sec
        
        if seconds < 60:
            time_str = f"{seconds:.1f} seconds"
        elif seconds < 3600:
            time_str = f"{seconds/60:.1f} minutes"
        else:
            time_str = f"{seconds/3600:.1f} hours"
        
        response = messagebox.askyesno(
            "Performance Warning!",
            f"{algorithm} with {n:,} recorded data may take approximately {time_str} to sort.   Σ(°ロ°)\n\n"
            f"Would you like to continue anyway? "
        )
        
        return response

if __name__ == "__main__":
    app = SortingBenchmarkApp()
    app.mainloop()