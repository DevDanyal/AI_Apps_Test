import tkinter as tk
from tkinter import colorchooser

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Paint Application")

        self.brush_size = 5
        self.color = "black"
        self.tool = "pencil"
        self.start_x = None
        self.start_y = None

        # --- UI Elements ---
        # Control Frame
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Color Chooser
        self.color_button = tk.Button(self.control_frame, text="Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Brush Size
        self.brush_size_slider = tk.Scale(self.control_frame, from_=1, to=20, orient=tk.HORIZONTAL, label="Brush Size", command=self.set_brush_size)
        self.brush_size_slider.set(self.brush_size)
        self.brush_size_slider.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Tool Selection
        self.tool_label = tk.Label(self.control_frame, text="Tool:")
        self.tool_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.pencil_button = tk.Button(self.control_frame, text="Pencil", command=lambda: self.set_tool("pencil"))
        self.pencil_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.line_button = tk.Button(self.control_frame, text="Line", command=lambda: self.set_tool("line"))
        self.line_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.rectangle_button = tk.Button(self.control_frame, text="Rectangle", command=lambda: self.set_tool("rectangle"))
        self.rectangle_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Clear Button
        self.clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Canvas for drawing
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()
        
        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def choose_color(self):
        self.color = colorchooser.askcolor(color=self.color)[1]

    def set_brush_size(self, size):
        self.brush_size = int(size)

    def set_tool(self, tool):
        self.tool = tool

    def clear_canvas(self):
        self.canvas.delete("all")

    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def stop_drawing(self, event):
        if self.tool == "line":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.brush_size)
        elif self.tool == "rectangle":
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.brush_size)
        
        self.start_x = None
        self.start_y = None

    def paint(self, event):
        if self.tool == "pencil":
            if self.start_x and self.start_y:
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, 
                                        fill=self.color, width=self.brush_size, 
                                        capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
            self.start_x = event.x
            self.start_y = event.y

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
