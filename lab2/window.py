import tkinter as tk
from editor import Editor

class Window():
    def __init__(self, root):
        self.root = root
        self.root.title("OOP_lab2 - [Прямокутник]")
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

        objects_menu = tk.Menu(menubar, tearoff=0)
        objects_menu.add_command(label="Крапка", command=lambda: self.select_shape("Point"))
        objects_menu.add_command(label="Лінія", command=lambda: self.select_shape("Line"))
        objects_menu.add_command(label="Прямокутник", command=lambda: self.select_shape("Rectangle"))
        objects_menu.add_command(label="Еліпс", command=lambda: self.select_shape("Ellipse"))
        menubar.add_cascade(label="Об’єкти", menu=objects_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.show_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

    def select_shape(self, type):
        self.editor.set_shape_type(type)
        self.root.title(f"OOP_lab2 - {type}")


    def show_about(self):
        print("Лабораторна робота №2 з ООП")
