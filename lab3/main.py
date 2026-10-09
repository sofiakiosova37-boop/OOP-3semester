import tkinter as tk
from window import Window

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = Window(root)
    root.mainloop()