import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import matplotlib.pyplot as plt

class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Power Prediction GUI")
        self.root.geometry("800x600")

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Example buttons for different plots
        self.btn1 = ttk.Button(self.button_frame, text="Show Sine Plot", command=self.show_sine_plot)
        self.btn1.pack(side=tk.LEFT, padx=5)

        self.btn2 = ttk.Button(self.button_frame, text="Show Cosine Plot", command=self.show_cosine_plot)
        self.btn2.pack(side=tk.LEFT, padx=5)

        self.canvas = None

    def show_sine_plot(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self._draw_plot(x, y, "Sine Plot")

    def show_cosine_plot(self):
        x = np.linspace(0, 10, 100)
        y = np.cos(x)
        self._draw_plot(x, y, "Cosine Plot")

    def _draw_plot(self, x, y, title):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y)
        ax.set_title(title)
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    def run(self):
        self.root.mainloop()

