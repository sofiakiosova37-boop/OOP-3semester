
import os
import socket
import subprocess
import sys
import time
import tkinter as tk
from tkinter import messagebox

HOST = "127.0.0.1"
PORT_OBJECT2 = 50002
PORT_OBJECT3 = 50003
DIR = os.path.dirname(os.path.abspath(__file__))

def send_command(port, command, timeout=5.0):
    try:
        with socket.create_connection((HOST, port), timeout=timeout) as sock:
            sock.sendall((command + "\n").encode("utf-8"))
            return sock.makefile("r", encoding="utf-8").readline().strip()
    except OSError:
        return None

def is_running(port):
    return send_command(port, "PING", timeout=1.0) == "OK"

def ensure_running(port, script):
    if is_running(port):
        return True
    subprocess.Popen([sys.executable, os.path.join(DIR, script)])
    for _ in range(50): 
        time.sleep(0.1)
        if is_running(port):
            return True
    return False

def run_work(n, lo, hi):
    status.config(text="Виконується...")
    root.update()

    if not ensure_running(PORT_OBJECT2, "object2.py") or not ensure_running(PORT_OBJECT3, "object3.py"):
        status.config(text="Помилка запуску Object2/Object3")
        messagebox.showerror("Помилка", "Не вдалося запустити Object2/Object3.")
        return

    send_command(PORT_OBJECT2, "MOVE 420 50")
    send_command(PORT_OBJECT3, "MOVE 420 420")

    reply = send_command(PORT_OBJECT2, f"GENERATE {n} {lo} {hi}")
    if reply != "OK":
        status.config(text="Помилка Object2")
        messagebox.showerror("Помилка Object2", str(reply))
        return

    reply = send_command(PORT_OBJECT3, "COMPUTE")
    if reply != "OK":
        status.config(text="Помилка Object3")
        messagebox.showerror("Помилка Object3", str(reply))
        return
    status.config(text=f"Готово: матриця {n}x{n}, діапазон [{lo}; {hi}]")

def open_dialog():
    dlg = tk.Toplevel(root)
    dlg.title("Параметри")
    dlg.transient(root)
    dlg.resizable(False, False)
    dlg.geometry(f"+{root.winfo_x() + 40}+{root.winfo_y() + 40}")
    frame = tk.Frame(dlg, padx=20, pady=15)
    frame.pack()
    tk.Label(frame, text="n (розмір матриці):").grid(row=0, column=0, sticky="e", pady=4)
    tk.Label(frame, text="Min:").grid(row=1, column=0, sticky="e", pady=4)
    tk.Label(frame, text="Max:").grid(row=2, column=0, sticky="e", pady=4)

    entries = []
    for row, var in enumerate((var_n, var_min, var_max)):
        e = tk.Entry(frame, width=10, textvariable=var)
        e.grid(row=row, column=1, padx=8)
        entries.append(e)
    entries[0].focus_set()

    def on_ok():
        try:
            n, lo, hi = int(var_n.get()), int(var_min.get()), int(var_max.get())
        except ValueError:
            messagebox.showerror("Помилка", "Введіть цілі числа в усі поля.", parent=dlg)
            return
        if n < 1 or lo > hi:
            messagebox.showerror("Помилка", "Потрібно n >= 1 та Min <= Max.", parent=dlg)
            return
        dlg.destroy()
        run_work(n, lo, hi)

    buttons = tk.Frame(frame)
    buttons.grid(row=3, column=0, columnspan=2, pady=(12, 0))
    tk.Button(buttons, text="Виконати", width=10, command=on_ok).pack(side="left", padx=4)
    tk.Button(buttons, text="Скасувати", width=10, command=dlg.destroy).pack(side="left", padx=4)
    dlg.bind("<Return>", lambda e: on_ok())
    dlg.bind("<Escape>", lambda e: dlg.destroy())
    dlg.grab_set()  

def on_close():
    send_command(PORT_OBJECT2, "QUIT", timeout=1.0)
    send_command(PORT_OBJECT3, "QUIT", timeout=1.0)
    root.destroy()

root = tk.Tk()
root.title("Lab6")
root.geometry("340x110+50+50")
root.protocol("WM_DELETE_WINDOW", on_close)

var_n = tk.StringVar(value="4")
var_min = tk.StringVar(value="-10")
var_max = tk.StringVar(value="10")

menubar = tk.Menu(root)
work_menu = tk.Menu(menubar, tearoff=0)
work_menu.add_command(label="Виконати...", command=open_dialog)
work_menu.add_separator()
work_menu.add_command(label="Вихід", command=on_close)
menubar.add_cascade(label="Робота", menu=work_menu)
root.config(menu=menubar)

tk.Label(root, text="Оберіть пункт меню\n«Робота → Виконати...»", font=("Arial", 11)).pack(pady=(15, 5))
status = tk.Label(root, text="", fg="gray")
status.pack()

root.mainloop()