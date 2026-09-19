## Module for option 2 (Next+Cancel btn)
import tkinter as tk

class Module2_step1(tk.Toplevel):
    def __init__(self, parent, callback_func ):
        super().__init__(parent)
        self.callback_function = callback_func
        self.title("Module2_step1")
        self.geometry("250x200")
        tk.Label(self, text="Перше вікно").pack()
        tk.Button(self, text="Далі", command=self._on_next).pack(side=tk.LEFT)
        tk.Button(self, text="Відміна", command=self.destroy).pack(side=tk.RIGHT)

    def _on_next(self):
        self.destroy()
        self.callback_function()
