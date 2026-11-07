import tkinter as tk
from editor import Editor
import os
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from additionalwindow import ShapesTable
import csv
from shapes import Point, Line, Rectangle, Ellipse, line_circles, Cube

shape_classes = {
    "Point": Point,
    "Line": Line,
    "Rectangle": Rectangle,
    "Ellipse": Ellipse,
    "line_circles": line_circles,
    "Cube": Cube,
}

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
        self.highlight_id = None #
        self.editor.canvas.bind('<ButtonRelease-1>', self.on_canvas_release, add="+")
        self.table = None
        self.icons = {}
        self.buttons = {}
        self.create_menu()
        self.create_toolbar()
        self.select_shape("Rectangle")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        #file_menu = tk.Menu(menubar, tearoff=0)
        #file_menu.add_command(label="Вихід", command=self.root.quit)
        #menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Відкрити...", command=self.load_file)
        file_menu.add_command(label="Зберегти як...", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.exit_app)

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
        self.table_var = tk.BooleanVar(value=False)
        table_menu = tk.Menu(menubar, tearoff=0)
        table_menu.add_checkbutton(label="Показати таблицю", variable=self.table_var, command=self.toggle_table) # table_menu.add_command(label="Показати таблицю", command=self.toggle_table)
        menubar.add_cascade(label="Таблиця", menu=table_menu)
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
        self.root.title(f"OOP_lab5 - {type}")

    def toggle_table(self):
        if self.table_var.get():
            if self.table is None:
                self.table = ShapesTable(self.root,  on_select=self.table_select, on_delete=self.table_delete, on_edit=self.table_edit, on_close=self.on_table_closed)
                self.table.refresh(self.editor.shapes)
        else:
            if self.table is not None:
                self.table.close()

    def on_table_closed(self):
        self.clear_highlight()
        self.table = None
        self.table_var.set(False)

    def on_canvas_release(self, event):
        if self.table:
            self.table.refresh(self.editor.shapes)

    def redraw(self):
        self.editor.redraw()
        self.highlight_id = None      
        if self.table:
            self.table.refresh(self.editor.shapes)

    def table_select(self, index):
        if index is None:
            self.clear_highlight()
        else:
            self.highlight_shape(index)

    def table_delete(self, index):
        del self.editor.shapes[index]
        self.redraw()

    def table_edit(self, index, col_name, value):
        setattr(self.editor.shapes[index], col_name, value)
        self.redraw()
        self.table.select_row(index)

    def clear_highlight(self):
        if self.highlight_id:
            self.editor.canvas.delete(self.highlight_id)
            self.highlight_id = None

    def highlight_shape(self, index):
        self.clear_highlight()
        canvas = self.editor.canvas
        count = len(canvas.find_all())
        self.editor.shapes[index].draw(canvas)
        new_ids = canvas.find_all()[count:]
        x1, y1, x2, y2 = canvas.bbox(*new_ids)
        canvas.delete(*new_ids)
        self.highlight_id = canvas.create_rectangle(x1 - 4, y1 - 4, x2 + 4, y2 + 4, outline="red", width=2, dash=(4, 2))

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="data.csv", filetypes=[("CSV", "*.csv")])
        if path:
            # self.editor.save_csv(path)
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for s in self.editor.shapes:
                    writer.writerow([type(s).__name__, s.x1, s.y1, s.x2, s.y2])
            return True 
        return False  
    
    def exit_app(self):
        print("exit_app вызван")
        answer = self.ask_save()
        if answer == "cancel":
            return                      # лишаємось у програмі
        if answer == "save" and not self.save_file():
            return                      # обрали "Зберегти", але скасували вікно збереження
        if self.table is not None:
            self.table.close()
        self.root.destroy()

    def ask_save(self):
        """Повертає 'save', 'discard' або 'cancel'."""
        result = {"value": "cancel"}

        dialog = tk.Toplevel(self.root)
        dialog.title("OOP_lab5")
        dialog.resizable(False, False)
        dialog.transient(self.root)

        # розмір і центрування відносно головного вікна
        w, h = 420, 190
        x = self.root.winfo_x() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - h) // 2
        dialog.geometry(f"{w}x{h}+{x}+{y}")

        # верхня біла частина
        top = tk.Frame(dialog, bg="white")
        top.pack(fill=tk.BOTH, expand=True)
        tk.Label(top, text="Зберегти роботу?", font=("Segoe UI", 14, "bold"),
                 bg="white", anchor="w").pack(fill=tk.X, padx=20, pady=(20, 5))
        tk.Label(top, text='У файлі "Без імені" є незбережені зміни.',
                 font=("Segoe UI", 10), bg="white", anchor="w").pack(fill=tk.X, padx=20)

        tk.Frame(dialog, height=1, bg="#e0e0e0").pack(fill=tk.X)   # лінія-роздільник

        # нижня сіра частина з кнопками
        bottom = tk.Frame(dialog, bg="#f3f3f3")
        bottom.pack(fill=tk.X)

        def choose(value):
            result["value"] = value
            dialog.destroy()

        tk.Button(bottom, text="Зберегти", bg="#0067c0", fg="white",
                  activebackground="#005a9e", activeforeground="white",
                  relief=tk.FLAT, command=lambda: choose("save")
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(20, 5), pady=15, ipady=4)
        tk.Button(bottom, text="Не зберігати", bg="white", relief=tk.SOLID, bd=1,
                  command=lambda: choose("discard")
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=15, ipady=4)
        tk.Button(bottom, text="Скасувати", bg="white", relief=tk.SOLID, bd=1,
                  command=lambda: choose("cancel")
                  ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 20), pady=15, ipady=4)

        dialog.protocol("WM_DELETE_WINDOW", lambda: choose("cancel"))  # хрестик діалогу = скасувати
        dialog.grab_set()                 # поки діалог відкритий, головне вікно недоступне
        self.root.wait_window(dialog)     # чекаємо, поки діалог закриють
        return result["value"]

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            try:
                shapes = []
                with open(path, newline="", encoding="utf-8") as f:
                    for row in csv.reader(f):
                        if len(row) != 5 or row[0] not in shape_classes:
                            continue
                        shapes.append(shape_classes[row[0]](int(row[1]), int(row[2]), int(row[3]), int(row[4])))
                self.editor.shapes = shapes
                self.redraw()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося прочитати файл:\n{e}")

    def show_about(self):
        print("Лабораторна робота №5 з ООП")