import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math
import os
import time
from datetime import datetime

class DivideConquerVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Divide & Conquer Algorithm Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg="#000000")  # Black background
        
        # Track algorithm steps and points
        self.steps = []
        self.execution_time = 0
        self.comparisons = 0
        self.points = []  # Store points for visualization
        self.closest_pair = None  # Store closest pair
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#1a1a1a", relief=tk.RAISED, bd=2)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(header_frame, text="🔬 Divide & Conquer Algorithm Visualizer",
                font=("Arial", 20, "bold"), bg="#1a1a1a", fg="#00ffff").pack(pady=10)  # Cyan color
        
        tk.Label(header_frame, text="Advanced Implementation with Step-by-Step Analysis",
                font=("Arial", 11), bg="#1a1a1a", fg="#ff9900").pack(pady=5)  # Orange color
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg="#000000")  # Black background
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left Panel - Controls
        left_panel = tk.Frame(content_frame, bg="#1a1a1a", relief=tk.GROOVE, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        tk.Label(left_panel, text="Control Panel", font=("Arial", 14, "bold"),
                bg="#1a1a1a", fg="#ffffff").pack(pady=10)  # White
        
        # Algorithm Selection
        tk.Label(left_panel, text="Select Algorithm:", font=("Arial", 10, "bold"),
                bg="#1a1a1a", fg="#ff9900").pack(pady=5)  # Orange
        
        self.algo_var = tk.StringVar(value="auto")
        algos = [("Auto Detect", "auto"), 
                ("Closest Pair of Points", "closest"), 
                ("Integer Multiplication", "integer")]
        
        for text, value in algos:
            tk.Radiobutton(left_panel, text=text, variable=self.algo_var, value=value,
                          bg="#1a1a1a", fg="#00ffff", selectcolor="#333333",  # Cyan text
                          font=("Arial", 9), activebackground="#1a1a1a").pack(anchor=tk.W, padx=20)
        
        # File Selection Button
        tk.Button(left_panel, text="📁 Select Input File", command=self.select_file,
                 bg="#0066cc", fg="white", font=("Arial", 11, "bold"),  # Blue button
                 padx=20, pady=10, relief=tk.RAISED, bd=3, activebackground="#004499").pack(pady=15)
        
        # Run Button
        tk.Button(left_panel, text="▶ Run Algorithm", command=self.run_algorithm,
                 bg="#00aa00", fg="white", font=("Arial", 11, "bold"),  # Green button
                 padx=20, pady=10, relief=tk.RAISED, bd=3, activebackground="#008800").pack(pady=5)
        
        # Clear Button
        tk.Button(left_panel, text="🗑 Clear Results", command=self.clear_results,
                 bg="#cc0000", fg="white", font=("Arial", 11, "bold"),  # Red button
                 padx=20, pady=10, relief=tk.RAISED, bd=3, activebackground="#990000").pack(pady=5)
        
        # Statistics Frame
        stats_frame = tk.LabelFrame(left_panel, text="Statistics", bg="#1a1a1a",
                                   fg="#ff9900", font=("Arial", 10, "bold"))  # Orange
        stats_frame.pack(pady=15, padx=10, fill=tk.X)
        
        self.stats_label = tk.Label(stats_frame, text="No data loaded",
                                   bg="#1a1a1a", fg="#00ffff", font=("Arial", 9),  # Cyan
                                   justify=tk.LEFT)
        self.stats_label.pack(pady=5)
        
        # Right Panel - Results
        right_panel = tk.Frame(content_frame, bg="#000000")  # Black
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Style for notebook with black theme
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background="#000000")
        style.configure('TNotebook.Tab', background="#333333", foreground="#00ffff",  # Dark gray, cyan text
                       padding=[10, 5], font=("Arial", 9, "bold"))
        style.map('TNotebook.Tab', 
                 background=[('selected', '#006666')],  # Dark cyan when selected
                 foreground=[('selected', '#ffffff')])  # White text when selected
        
        # Results Tab
        results_frame = tk.Frame(self.notebook, bg="#000000")
        self.notebook.add(results_frame, text="📊 Results")
        
        self.result_text = tk.Text(results_frame, height=20, width=70,
                                   font=("Consolas", 10), bg="#1a1a1a", fg="#ffffff",  # White text
                                   relief=tk.SUNKEN, bd=2)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        result_scroll = tk.Scrollbar(results_frame, command=self.result_text.yview)
        result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=result_scroll.set)
        
        # Steps Tab
        steps_frame = tk.Frame(self.notebook, bg="#000000")
        self.notebook.add(steps_frame, text="📝 Algorithm Steps")
        
        self.steps_text = tk.Text(steps_frame, height=20, width=70,
                                 font=("Consolas", 9), bg="#1a1a1a", fg="#ff9900",  # Orange text
                                 relief=tk.SUNKEN, bd=2)
        self.steps_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        steps_scroll = tk.Scrollbar(steps_frame, command=self.steps_text.yview)
        steps_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.steps_text.config(yscrollcommand=steps_scroll.set)
        
        # Input Data Tab
        input_frame = tk.Frame(self.notebook, bg="#000000")
        self.notebook.add(input_frame, text="📄 Input Data")
        
        self.input_text = tk.Text(input_frame, height=20, width=70,
                                 font=("Consolas", 9), bg="#1a1a1a", fg="#00ffff",  # Cyan text
                                 relief=tk.SUNKEN, bd=2)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        input_scroll = tk.Scrollbar(input_frame, command=self.input_text.yview)
        input_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.config(yscrollcommand=input_scroll.set)
        
        # NEW: Visualization Tab
        visualization_frame = tk.Frame(self.notebook, bg="#000000")
        self.notebook.add(visualization_frame, text="🎨 Visualization")
        
        # Visualization controls
        viz_control_frame = tk.Frame(visualization_frame, bg="#000000")
        viz_control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(viz_control_frame, text="Visualization Controls:", 
                bg="#000000", fg="#ffffff", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.viz_scale = tk.DoubleVar(value=1.0)
        tk.Scale(viz_control_frame, from_=0.5, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
                variable=self.viz_scale, label="Zoom:", bg="#000000", fg="#ffffff",
                troughcolor="#333333", command=self.update_visualization).pack(side=tk.LEFT, padx=20)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(visualization_frame, bg="#000000", highlightthickness=1,
                               highlightbackground="#333333")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", relief=tk.SUNKEN,
                                  anchor=tk.W, bg="#1a1a1a", fg="#ff9900",  # Orange
                                  font=("Arial", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.current_file = None
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
            
        self.current_file = file_path
        self.status_bar.config(text=f"Loaded: {os.path.basename(file_path)}")
        
        # Display input data
        with open(file_path, 'r') as f:
            data = f.read()
        
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, f"File: {os.path.basename(file_path)}\n")
        self.input_text.insert(tk.END, f"{'='*60}\n\n")
        self.input_text.insert(tk.END, data)
        
        messagebox.showinfo("Success", f"File loaded successfully!\n{os.path.basename(file_path)}")
    
    def clear_results(self):
        self.result_text.delete("1.0", tk.END)
        self.steps_text.delete("1.0", tk.END)
        self.input_text.delete("1.0", tk.END)
        self.stats_label.config(text="No data loaded")
        self.status_bar.config(text="Ready")
        self.steps = []
        self.points = []
        self.closest_pair = None
        self.canvas.delete("all")
        
    def run_algorithm(self):
        if not self.current_file:
            messagebox.showerror("Error", "Please select an input file first!")
            return
        
        self.steps = []
        self.comparisons = 0
        self.points = []
        self.closest_pair = None
        
        try:
            with open(self.current_file, 'r') as f:
                data = f.read().strip().split()
            
            # Detect algorithm type
            algo_type = self.algo_var.get()
            if algo_type == "auto":
                if "closest" in self.current_file.lower():
                    algo_type = "closest"
                elif "integer" in self.current_file.lower():
                    algo_type = "integer"
                else:
                    messagebox.showerror("Error", "Cannot auto-detect algorithm. Please select manually.")
                    return
            
            start_time = time.time()
            
            if algo_type == "closest":
                self.run_closest_pair(data)
                # Switch to visualization tab after running closest pair
                self.notebook.select(3)  # Index 3 is the visualization tab
                self.update_visualization()
            elif algo_type == "integer":
                self.run_integer_multiplication(data)
            
            self.execution_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Update statistics
            self.update_statistics(algo_type, len(data))
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_bar.config(text=f"Error: {str(e)}")
    
    def run_closest_pair(self, data):
        self.points = [(float(data[i]), float(data[i + 1])) for i in range(0, len(data), 2)]
        points_sorted = sorted(self.points, key=lambda x: x[0])
        
        self.steps.append("="*60)
        self.steps.append("CLOSEST PAIR OF POINTS ALGORITHM")
        self.steps.append("="*60)
        self.steps.append(f"\nInput: {len(points_sorted)} points")
        self.steps.append(f"Points (sorted by x-coordinate):")
        for i, p in enumerate(points_sorted[:10]):  # Show first 10
            self.steps.append(f"  {i+1}. ({p[0]:.2f}, {p[1]:.2f})")
        if len(points_sorted) > 10:
            self.steps.append(f"  ... and {len(points_sorted)-10} more points")
        
        dist, pair = self.closest_pair_recursive(points_sorted, 0)
        self.closest_pair = pair
        
        # Display results
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "╔" + "═"*58 + "╗\n")
        self.result_text.insert(tk.END, "║  CLOSEST PAIR OF POINTS - RESULTS" + " "*23 + "║\n")
        self.result_text.insert(tk.END, "╚" + "═"*58 + "╝\n\n")
        
        self.result_text.insert(tk.END, f"File: {os.path.basename(self.current_file)}\n")
        self.result_text.insert(tk.END, f"Algorithm: Divide & Conquer\n")
        self.result_text.insert(tk.END, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        self.result_text.insert(tk.END, "─"*60 + "\n\n")
        
        self.result_text.insert(tk.END, f"Total Points Analyzed: {len(points_sorted)}\n")
        self.result_text.insert(tk.END, f"Comparisons Made: {self.comparisons}\n")
        self.result_text.insert(tk.END, f"Execution Time: {self.execution_time:.4f} ms\n\n")
        self.result_text.insert(tk.END, "─"*60 + "\n\n")
        
        self.result_text.insert(tk.END, "🎯 CLOSEST PAIR FOUND:\n\n")
        self.result_text.insert(tk.END, f"  Point 1: ({pair[0][0]:.6f}, {pair[0][1]:.6f})\n")
        self.result_text.insert(tk.END, f"  Point 2: ({pair[1][0]:.6f}, {pair[1][1]:.6f})\n\n")
        self.result_text.insert(tk.END, f"  Distance: {dist:.8f}\n\n")
        self.result_text.insert(tk.END, "─"*60 + "\n\n")
        
        self.result_text.insert(tk.END, "✓ Algorithm completed successfully!\n")
        
        # Display steps
        self.steps_text.delete("1.0", tk.END)
        self.steps_text.insert(tk.END, "\n".join(self.steps))
        
        self.status_bar.config(text=f"Completed: Closest Pair | Distance: {dist:.4f}")
    
    def closest_pair_recursive(self, points, depth):
        indent = "  " * depth
        
        if len(points) <= 3:
            self.steps.append(f"\n{indent}Base case: {len(points)} points - using brute force")
            dist, pair = self.brute_force_closest(points)
            self.steps.append(f"{indent}  → Minimum distance: {dist:.4f}")
            return dist, pair
        
        mid = len(points) // 2
        self.steps.append(f"\n{indent}Dividing {len(points)} points at index {mid}")
        self.steps.append(f"{indent}  Left: {len(points[:mid])} points")
        self.steps.append(f"{indent}  Right: {len(points[mid:])} points")
        
        dleft, pair_left = self.closest_pair_recursive(points[:mid], depth + 1)
        dright, pair_right = self.closest_pair_recursive(points[mid:], depth + 1)
        
        d = min(dleft, dright)
        best_pair = pair_left if dleft < dright else pair_right
        
        self.steps.append(f"{indent}Merging: min({dleft:.4f}, {dright:.4f}) = {d:.4f}")
        
        # Check strip
        mid_x = points[mid][0]
        strip = [p for p in points if abs(p[0] - mid_x) < d]
        strip.sort(key=lambda x: x[1])
        
        self.steps.append(f"{indent}Checking strip: {len(strip)} points within distance {d:.4f}")
        
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 7, len(strip))):
                dist = self.distance(strip[i], strip[j])
                self.comparisons += 1
                if dist < d:
                    d = dist
                    best_pair = (strip[i], strip[j])
                    self.steps.append(f"{indent}  ✓ New minimum found: {d:.4f}")
        
        return d, best_pair
    
    def brute_force_closest(self, points):
        min_dist = float('inf')
        pair = None
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                d = self.distance(points[i], points[j])
                self.comparisons += 1
                if d < min_dist:
                    min_dist = d
                    pair = (points[i], points[j])
        return min_dist, pair
    
    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
    def update_visualization(self, event=None):
        """Update the visualization canvas with points and connections"""
        self.canvas.delete("all")
        
        if not self.points:
            # Show message when no points
            self.canvas.create_text(300, 200, 
                                   text="No points to visualize.\nRun Closest Pair algorithm first.",
                                   fill="#ffffff", font=("Arial", 14), justify="center")
            return
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 600, 400
        
        # Find bounds of points
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # Add some padding
        range_x = max_x - min_x
        range_y = max_y - min_y
        
        if range_x == 0:
            range_x = 1
        if range_y == 0:
            range_y = 1
        
        padding = 0.1
        min_x -= range_x * padding
        max_x += range_x * padding
        min_y -= range_y * padding
        max_y += range_y * padding
        range_x = max_x - min_x
        range_y = max_y - min_y
        
        # Apply zoom scale
        scale = self.viz_scale.get()
        
        # Draw grid
        grid_color = "#333333"
        for i in range(1, 10):
            x = (i * canvas_width / 10)
            y = (i * canvas_height / 10)
            self.canvas.create_line(x, 0, x, canvas_height, fill=grid_color, width=1)
            self.canvas.create_line(0, y, canvas_width, y, fill=grid_color, width=1)
        
        # Draw axes
        self.canvas.create_line(0, canvas_height/2, canvas_width, canvas_height/2, 
                               fill="#666666", width=2)  # X-axis
        self.canvas.create_line(canvas_width/2, 0, canvas_width/2, canvas_height, 
                               fill="#666666", width=2)  # Y-axis
        
        # Scale points to fit canvas
        def scale_point(x, y):
            scaled_x = ((x - min_x) / range_x) * canvas_width * scale
            scaled_y = canvas_height - ((y - min_y) / range_y) * canvas_height * scale
            # Center the points
            offset_x = (canvas_width - (canvas_width * scale)) / 2
            offset_y = (canvas_height - (canvas_height * scale)) / 2
            return scaled_x + offset_x, scaled_y + offset_y
        
        # Draw all points
        point_radius = 5
        for i, (x, y) in enumerate(self.points):
            sx, sy = scale_point(x, y)
            
            # Check if this point is part of the closest pair
            is_closest = False
            if self.closest_pair:
                if (abs(x - self.closest_pair[0][0]) < 0.0001 and abs(y - self.closest_pair[0][1]) < 0.0001) or \
                   (abs(x - self.closest_pair[1][0]) < 0.0001 and abs(y - self.closest_pair[1][1]) < 0.0001):
                    is_closest = True
            
            if is_closest:
                # Draw closest pair points in red with glow effect
                self.canvas.create_oval(sx - point_radius*2, sy - point_radius*2,
                                       sx + point_radius*2, sy + point_radius*2,
                                       fill="#ff0000", outline="#ff6666", width=3)
                self.canvas.create_text(sx, sy - 15, text=f"({x:.1f},{y:.1f})",
                                       fill="#ff6666", font=("Arial", 8, "bold"))
            else:
                # Draw regular points in cyan
                self.canvas.create_oval(sx - point_radius, sy - point_radius,
                                       sx + point_radius, sy + point_radius,
                                       fill="#00ffff", outline="#009999", width=2)
                if len(self.points) <= 20:  # Only label if not too many points
                    self.canvas.create_text(sx, sy - 10, text=f"P{i+1}",
                                           fill="#009999", font=("Arial", 7))
        
        # Draw the line connecting closest pair
        if self.closest_pair:
            x1, y1 = self.closest_pair[0]
            x2, y2 = self.closest_pair[1]
            sx1, sy1 = scale_point(x1, y1)
            sx2, sy2 = scale_point(x2, y2)
            
            # Draw the connecting line
            self.canvas.create_line(sx1, sy1, sx2, sy2, 
                                   fill="#ff9900", width=3, dash=(5, 2))
            
            # Add distance label
            mid_x = (sx1 + sx2) / 2
            mid_y = (sy1 + sy2) / 2
            dist = self.distance(self.closest_pair[0], self.closest_pair[1])
            self.canvas.create_text(mid_x, mid_y - 10, 
                                   text=f"Distance: {dist:.4f}", 
                                   fill="#ff9900", font=("Arial", 9, "bold"))
        
        # Draw legend
        legend_x, legend_y = 10, 10
        self.canvas.create_rectangle(legend_x, legend_y, legend_x + 150, legend_y + 90,
                                    fill="#1a1a1a", outline="#666666", width=1)
        self.canvas.create_text(legend_x + 75, legend_y + 15, text="Legend",
                               fill="#ffffff", font=("Arial", 9, "bold"))
        
        # Regular points
        self.canvas.create_oval(legend_x + 10, legend_y + 30, legend_x + 25, legend_y + 45,
                               fill="#00ffff", outline="#009999")
        self.canvas.create_text(legend_x + 40, legend_y + 37, text="Points",
                               fill="#ffffff", font=("Arial", 8), anchor="w")
        
        # Closest pair points
        self.canvas.create_oval(legend_x + 10, legend_y + 50, legend_x + 25, legend_y + 65,
                               fill="#ff0000", outline="#ff6666")
        self.canvas.create_text(legend_x + 40, legend_y + 57, text="Closest Pair",
                               fill="#ffffff", font=("Arial", 8), anchor="w")
        
        # Connecting line
        self.canvas.create_line(legend_x + 10, legend_y + 75, legend_x + 25, legend_y + 75,
                               fill="#ff9900", width=2)
        self.canvas.create_text(legend_x + 40, legend_y + 75, text="Min Distance",
                               fill="#ffffff", font=("Arial", 8), anchor="w")
    
    def run_integer_multiplication(self, data):
        x, y = int(data[0]), int(data[1])
        
        self.steps.append("="*60)
        self.steps.append("KARATSUBA INTEGER MULTIPLICATION ALGORITHM")
        self.steps.append("="*60)
        self.steps.append(f"\nInput Numbers:")
        self.steps.append(f"  X = {x}")
        self.steps.append(f"  Y = {y}")
        self.steps.append(f"\nDigits: X has {len(str(x))} digits, Y has {len(str(y))} digits")
        
        product = self.karatsuba_multiply(x, y, 0)
        
        # Verify with standard multiplication
        expected = x * y
        is_correct = (product == expected)
        
        # Display results
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "╔" + "═"*58 + "╗\n")
        self.result_text.insert(tk.END, "║  KARATSUBA INTEGER MULTIPLICATION - RESULTS" + " "*12 + "║\n")
        self.result_text.insert(tk.END, "╚" + "═"*58 + "╝\n\n")
        
        self.result_text.insert(tk.END, f"File: {os.path.basename(self.current_file)}\n")
        self.result_text.insert(tk.END, f"Algorithm: Karatsuba (Divide & Conquer)\n")
        self.result_text.insert(tk.END, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        self.result_text.insert(tk.END, "─"*60 + "\n\n")
        
        self.result_text.insert(tk.END, "INPUT:\n")
        self.result_text.insert(tk.END, f"  X = {x}\n")
        self.result_text.insert(tk.END, f"  Y = {y}\n\n")
        self.result_text.insert(tk.END, f"  X length: {len(str(x))} digits\n")
        self.result_text.insert(tk.END, f"  Y length: {len(str(y))} digits\n\n")
        self.result_text.insert(tk.END, "─"*60 + "\n\n")
        
        self.result_text.insert(tk.END, "OUTPUT:\n")
        self.result_text.insert(tk.END, f"  Product = {product}\n\n")
        self.result_text.insert(tk.END, f"  Result length: {len(str(product))} digits\n\n")
        self.result_text.insert(tk.END, "─"*60 + "\n\n")
        
        self.result_text.insert(tk.END, "VERIFICATION:\n")
        self.result_text.insert(tk.END, f"  Standard multiplication: {expected}\n")
        self.result_text.insert(tk.END, f"  Karatsuba result:        {product}\n")
        self.result_text.insert(tk.END, f"  Match: {'✓ CORRECT' if is_correct else '✗ ERROR'}\n\n")
        self.result_text.insert(tk.END, "─"*60 + "\n\n")
        
        self.result_text.insert(tk.END, f"Recursive Calls: {self.comparisons}\n")
        self.result_text.insert(tk.END, f"Execution Time: {self.execution_time:.4f} ms\n\n")
        self.result_text.insert(tk.END, "✓ Algorithm completed successfully!\n")
        
        # Display steps
        self.steps_text.delete("1.0", tk.END)
        self.steps_text.insert(tk.END, "\n".join(self.steps))
        
        self.status_bar.config(text=f"Completed: Integer Multiplication | Correct: {is_correct}")
    
    def karatsuba_multiply(self, x, y, depth):
        indent = "  " * depth
        self.comparisons += 1
        
        if x < 10 or y < 10:
            result = x * y
            self.steps.append(f"{indent}Base case: {x} × {y} = {result}")
            return result
        
        n = max(len(str(x)), len(str(y)))
        half = n // 2
        
        high1, low1 = divmod(x, 10 ** half)
        high2, low2 = divmod(y, 10 ** half)
        
        self.steps.append(f"\n{indent}Step {self.comparisons}:")
        self.steps.append(f"{indent}  X = {x} → high={high1}, low={low1}")
        self.steps.append(f"{indent}  Y = {y} → high={high2}, low={low2}")
        
        z0 = self.karatsuba_multiply(low1, low2, depth + 1)
        z1 = self.karatsuba_multiply((low1 + high1), (low2 + high2), depth + 1)
        z2 = self.karatsuba_multiply(high1, high2, depth + 1)
        
        result = (z2 * 10 ** (2 * half)) + ((z1 - z2 - z0) * 10 ** half) + z0
        self.steps.append(f"{indent}  → Result: {result}")
        
        return result
    
    def update_statistics(self, algo_type, data_size):
        stats = f"Algorithm: {algo_type.title()}\n"
        stats += f"Data Size: {data_size}\n"
        stats += f"Operations: {self.comparisons}\n"
        stats += f"Time: {self.execution_time:.4f} ms\n"
        
        if algo_type == "closest":
            complexity = f"O(n log n)\nn = {data_size//2}"
        else:
            complexity = f"O(n^1.585)\nn ≈ {max(len(str(data_size)), 2)}"
        
        stats += f"Complexity: {complexity}"
        
        self.stats_label.config(text=stats)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = DivideConquerVisualizer(root)
    root.mainloop()
    