## Module for option 2 (Back+Yes+Cancel btn)
import tkinter as tk

class Module2_step2(tk.Toplevel):
    def __init__(self, parent, callback_func ):
        super().__init__(parent)
        self.callback_function = callback_func
        self.title("Module2_step2")
        self.geometry("250x200")
        tk.Label(self, text="Друге вікно").pack()
        tk.Button(self, text="Назад", command=self._on_back).pack(side=tk.LEFT)
        tk.Button(self, text="Так", command=self.destroy).pack(side=tk.LEFT)
        tk.Button(self, text="Відміна", command=self.destroy).pack(side=tk.RIGHT)

    def _on_back(self):
        self.destroy()
        self.callback_function()
