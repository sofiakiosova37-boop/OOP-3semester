## Main module with visualization 
import tkinter as tk
import module1
import module2_step1
import module2_step2

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("300x150")

        main_menu = tk.Menu(self)
        main_menu.add_command(label="Module1", command=self.start_option1)
        main_menu.add_command(label="Module2", command=self.start_option2_step1)
        self.config(menu=main_menu)

        self.result=tk.Label(self, text="Число не обране")
        self.result.pack()

    def start_option1(self):
        module1.Module1(self, self.update_result)

    def update_result(self, value):
        self.result.config(text=f"Обране число: {value}")

    def start_option2_step1(self):
        module2_step1.Module2_step1(self, self.start_option2_step2)

    def start_option2_step2(self):
        module2_step2.Module2_step2(self, self.start_option2_step1)

if __name__ == "__main__":
    app = Main()
    app.mainloop()