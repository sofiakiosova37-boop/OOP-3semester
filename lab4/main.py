# number 13
import tkinter as tk
from editor import Editor
editor_instance = None

def main():
  global editor_instance
  root = tk.Tk()
  root.title("Графічний редактор")
  canvas = tk.Canvas(root, width=700, height=500, bg="white")
  canvas.pack(fill=tk.BOTH, expand=True)
  editor_instance = Editor(canvas)
  root.mainloop()

if __name__ == "__main__":
  main()