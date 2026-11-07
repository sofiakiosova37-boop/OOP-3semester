import tkinter as tk
from tkinter import ttk

class ShapesTable(tk.Toplevel):
    def __init__(self, master, on_close=None, on_delete=None, on_edit=None, on_select=None):
        super().__init__(master)
       # self.editor = editor
        self.on_select = on_select
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.on_close = on_close
        self.title("Таблиця об'єктів")
        self.geometry("400x300")

        tk.Button(self, text="Видалити виділений", command=self.delete_selected).pack(side=tk.BOTTOM, fill=tk.X)
        
        columns = ("type", "x1", "y1", "x2", "y2")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor=tk.CENTER)

        scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.protocol("WM_DELETE_WINDOW", self.close)  
        self.tree.bind("<<TreeviewSelect>>", self.handle_select)   # клік по рядку
        self.tree.bind("<Delete>", lambda e: self.delete_selected())  # клавіша Delete
        self.tree.bind("<Double-1>", self.on_double_click)   # редагування комірки
        # self.editor.table = self  
        # self.refresh()

    def refresh(self, shapes):
        self.tree.delete(*self.tree.get_children())
        for s in shapes:
            self.tree.insert("", tk.END, values=(type(s).__name__, s.x1, s.y1, s.x2, s.y2))
    
    def select_row(self, index):
        children = self.tree.get_children()
        if 0 <= index < len(children):
            self.tree.selection_set(children[index])

    def handle_select(self, event=None):
        if not self.on_select:
            return
        selected = self.tree.selection()
        if selected:
            self.on_select(self.tree.index(selected[0]))
        else:
            self.on_select(None)

    def delete_selected(self):
        selected = self.tree.selection()
        if selected and self.on_delete:
            self.on_delete(self.tree.index(selected[0]))

    def close(self):
        if self.on_close:
            self.on_close()
        self.destroy()

    def handle_select(self, event=None):
        if not self.on_select:
            return
        selected = self.tree.selection()
        if selected:
            self.on_select(self.tree.index(selected[0]))
        else:
            self.on_select(None)

    def delete_selected(self):
        selected = self.tree.selection()
        if selected:
            self.on_delete(self.tree.index(selected[0]))

    def on_double_click(self, event):
        if self.tree.identify_region(event.x, event.y) != "cell":
            return
        row = self.tree.identify_row(event.y)
        col_number = int(self.tree.identify_column(event.x)[1:]) - 1   
        if not row or col_number == 0:      
            return

        col_name = self.tree["columns"][col_number]   
        x, y, w, h = self.tree.bbox(row, "#" + str(col_number + 1))
        index = self.tree.index(row)

        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=w, height=h)
        entry.insert(0, self.tree.set(row, col_name))
        entry.focus()

        def save(event=None):
            try:
                value = int(entry.get())
            except ValueError:
                entry.destroy()          
                return
            entry.destroy()
            if self.on_edit:
                self.on_edit(index, col_name, value)

        entry.bind("<Return>", save)
        entry.bind("<Escape>", lambda e: entry.destroy())
        entry.bind("<FocusOut>", lambda e: entry.destroy())