import tkinter as tk
from lab2.editor import Editor

class Window():
    def __init__(self, root):
        self.root = root
        self.root.title("OOP_lab2 - [Прямокутник]")
        root = tk.Tk()
        root.title("Приклад з tk.Canvas")
        root.geometry("600x400") 
        canvas = tk.Canvas(root, bg="lightgray")
        canvas.pack(fill=tk.BOTH, expand=True)
        self.editor = Editor(canvas)
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Вихід", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        objects_menu = tk.Menu(menubar, tearoff=0)
        objects_menu.add_command()
