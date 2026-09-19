## Module for option 1
import tkinter as tk

class Module1(tk.Toplevel):
    def __init__(self, parent, callback_func):
        super().__init__(parent)
        self.callback_function = callback_func
        self.title("Module1")
        self.geometry("250x200")

        self.val_label = tk.Label(
            self, 
            text="30", 
            relief="solid", 
            bd=1, 
            width=6, 
            font=("Arial", 10)
        )
        self.val_label.pack()

        self.horizontalScale = tk.Scale(
            self, 
            orient=tk.HORIZONTAL,  
            from_=1.0, 
            to=100.0, 
            showvalue=0,
            command=self._update_label
        )
        self.horizontalScale.set(30)
        self.horizontalScale.pack(fill=tk.X)
        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM)
        tk.Button(btn_frame, text="Так", width=8, command=self._on_ok).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Відміна", width=8, command=self.destroy).pack(side=tk.RIGHT)

    def _on_ok(self):
        val = self.horizontalScale.get()
        self.callback_function(val)
        self.destroy()

    def _update_label(self, val):
        self.val_label.config(text=str(val))

