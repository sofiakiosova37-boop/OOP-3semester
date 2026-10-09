import tkinter as tk
from editor import Editor

class ToolTip():
    def __init__(self, widget, text):
        self.widget = widget
        self.text= text
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _cx, _cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify=tk.LEFT,
            background="#ffffe0", relief=tk.SOLID, borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class Window():
    def __init__(self, root):
        self.root = root
        self.root.title("OOP_lab3 - [Прямокутник]")
        root.geometry("600x400") 
        self.toolbar_frame = tk.Frame(root, bd=1, relief=tk.RAISED)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        canvas = tk.Canvas(root, bg="lightgray")
        canvas.pack(fill=tk.BOTH, expand=True)
        self.editor = Editor(canvas)
        
        self.icons = {}
        self.buttons = {}

        self.create_menu()
        self.create_toolbar()
        self.select_shape("Rectangle")

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Вихід", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        objects_menu = tk.Menu(menubar, tearoff=0)
        self.selected_type_var = tk.StringVar(value="Rectangle")

        shapes = [
            ("Крапка", "Point"),
            ("Лінія", "Line"),
            ("Прямокутник", "Rectangle"),
            ("Еліпс", "Ellipse")
        ]

        for label, shape_type in shapes:
            self.objects_menu.add_radiobutton(
                label=label,
                variable=self.selected_type_var,
                value=shape_type,
                command=lambda st=shape_type: self.select_shape(st)
            )
        
        menubar.add_cascade(label="Об’єкти", menu=objects_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.show_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

    def create_toolbar(self):
        tools = [
            ("Point", "Крапка", "dot.png"),
            ("Line", "Лінія", "line.png"),
            ("Rectangle", "Прямокутник", "rect.png"),
            ("Ellipse", "Еліпс", "ellipse.png")
        ]

    def select_shape(self, type):
        self.editor.set_shape_type(type)
        self.root.title(f"OOP_lab3 - {type}")


    def show_about(self):
        print("Лабораторна робота №3 з ООП")