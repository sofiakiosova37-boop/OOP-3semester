import tkinter as tk
from editor import Editor
import os
from PIL import Image, ImageTk

class ToolTip():
    def __init__(self, widget, text):
        self.widget = widget
        self.text= text
        self.tip_window = None
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
    def __init__(self, root, toolbar_frame=None):
        self.root = root
        self.root.title("OOP_lab3 - [Прямокутник]")
        root.geometry("600x400") 
        #self.toolbar_frame = tk.Frame(root, bd=1, relief=tk.RAISED)
        #self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        # canvas = tk.Canvas(root, bg="lightgray")
        # canvas.pack(fill=tk.BOTH, expand=True)
        #self.editor = Editor(canvas)
        #from editor import init_global_editor
        #self.editor = init_global_editor(canvas)
        if toolbar_frame is not None:
            self.toolbar_frame = toolbar_frame
        else:
            self.toolbar_frame = tk.Frame(root, bd=1, relief=tk.RAISED)
            self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        from editor import get_editor
        self.editor = get_editor()
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
        self.objects_menu = tk.Menu(menubar, tearoff=0)
        self.selected_type_var = tk.StringVar(value="Rectangle")

        shapes = [
            ("Крапка", "Point"),
            ("Лінія", "Line"),
            ("Прямокутник", "Rectangle"),
            ("Еліпс", "Ellipse"),
            ("Лінія з колами", "line_circles"),
            ("Куб", "Cube")
        ]

        for label, shape_type in shapes:
            self.objects_menu.add_radiobutton(
                label=label,
                variable=self.selected_type_var,
                value=shape_type,
                command=lambda st=shape_type: self.select_shape(st)
            )
        
        menubar.add_cascade(label="Об’єкти", menu=self.objects_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.show_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

    def create_toolbar(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        tools = [
            ("Point", "Крапка", "dot.png"),
            ("Line", "Лінія", "line.png"),
            ("Rectangle", "Прямокутник", "rectangle.png"),
            ("Ellipse", "Еліпс", "elipse.png"),
            ("line_circles", "Лінія з колами", "line_circles.png"),
            ("Cube", "Куб", "cube.png")
        ]

        for shape_type, tooltip_text, icon_file in tools:
            icon_path = os.path.join(base_dir, "images", icon_file)
            try:
                pil_img = Image.open(icon_path).resize((24, 24), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(pil_img)
                self.icons[shape_type] = img
                # img = tk.PhotoImage(file=icon_path)
                # img = img.subsample(4, 4)
               #  self.icons[shape_type] = img
                btn = tk.Button(
                    self.toolbar_frame, image=img, relief=tk.RAISED,
                    command=lambda st=shape_type: self.select_shape(st)
                )
            except Exception as e:
                print(f"Не вдалося завантажити іконку {icon_path}: {e}")
                btn = tk.Button(
                    self.toolbar_frame, text=shape_type[0], relief=tk.RAISED,
                    command=lambda st=shape_type: self.select_shape(st)
                )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            ToolTip(btn, tooltip_text)
            self.buttons[shape_type] = btn

    def select_shape(self, type):
        self.editor.set_shape_type(type)
        self.selected_type_var.set(type)
        for st, btn in self.buttons.items():
            if st == type:
                btn.config(relief=tk.SUNKEN) 
            else: 
                btn.config(relief=tk.RAISED)
        self.root.title(f"OOP_lab4 - {type}")

    def show_about(self):
        print("Лабораторна робота №4 з ООП")