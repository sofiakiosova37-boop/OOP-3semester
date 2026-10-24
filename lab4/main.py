import tkinter as tk
from window import Window
from editor import init_global_editor

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    toolbar_frame = tk.Frame(root, bd=1, relief=tk.RAISED)
    toolbar_frame.pack(side=tk.TOP, fill=tk.X)
    canvas = tk.Canvas(root, bg="lightgray")
    canvas.pack(fill=tk.BOTH, expand=True)
    init_global_editor(canvas)
    app = Window(root, toolbar_frame=toolbar_frame)
    root.mainloop()