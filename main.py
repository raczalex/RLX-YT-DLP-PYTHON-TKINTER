import tkinter as tk
from model.Model import Model
from controller.Controller import Controller
from pathlib import Path

if __name__ == "__main__":
    root = tk.Tk()
    model = Model()
    app = Controller(root, model)
    app.model.set_bin_path(Path(__file__).cwd() / 'bin')
    app.update_gui()  # Start updating the GUI
    app.download_bin_start()
    app.root.mainloop()