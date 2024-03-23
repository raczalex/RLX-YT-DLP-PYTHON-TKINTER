import tkinter as tk
from tkinter import ttk

class CustomProgressBar(ttk.Frame):
    def __init__(self, master, width=200, height=20, progress=0.0, bg_color="lightgray", progress_color="red", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.progress = progress
        self.bg_color = bg_color
        self.progress_color = progress_color
        self.draw_progress()

    def draw_progress(self):
        self.canvas.delete("progress")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        progress_normalized = self.progress / 100.0  # Scale progress to be between 0 and 1
        x0 = 0
        y0 = 0
        x1 = width * progress_normalized
        y1 = height
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.progress_color, outline="", tags="progress")
        self.canvas.create_rectangle(x1, y0, width, y1, fill=self.bg_color, outline="", tags="progress_bg")

    def set_progress(self, progress):
        self.progress = progress
        self.draw_progress()

    def get_progress(self):
        return self.progress