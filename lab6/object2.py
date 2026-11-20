"""Створення матриці та її відображення у вікні tkinter. Підтримка команд через сокет."""
import queue
import random
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import pyperclip  

HOST = "127.0.0.1"
PORT = 50002  # порт Object2

root = tk.Tk()
root.title("Object2")
root.geometry("+420+50")

title_label = tk.Label(root, text="Матриця ще не створена", font=("Arial", 11))
title_label.pack(padx=10, pady=(10, 0))

text_box = scrolledtext.ScrolledText(root, width=50, height=14, font=("Courier New", 11))
text_box.pack(padx=10, pady=10)
text_box.config(state="disabled")

tasks = queue.Queue()
def poll_tasks():
    while not tasks.empty():
        func, done, box = tasks.get()
        try:
            box["result"] = func()
        except Exception as e:
            box["error"] = str(e)
        done.set()
    root.after(50, poll_tasks)

def run_in_main(func):
    done, box = threading.Event(), {}
    tasks.put((func, done, box))
    done.wait(5)
    return box

def generate(n, lo, hi):
    matrix = [[random.randint(lo, hi) for _ in range(n)] for _ in range(n)]

    w = max(len(str(x)) for row in matrix for x in row)
    pretty = "\n".join(" ".join(str(x).rjust(w) for x in row) for row in matrix)
    title_label.config(text=f"Матриця {n}x{n}, діапазон [{lo}; {hi}]")
    text_box.config(state="normal")
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, pretty)
    text_box.config(state="disabled")

    pyperclip.copy("\n".join(" ".join(str(x) for x in row) for row in matrix))

def handle(command):
    parts = command.split()
    if not parts:
        return "ERROR empty"
    name = parts[0]

    if name == "PING":
        return "OK"
    if name == "GENERATE":
        try:
            n, lo, hi = int(parts[1]), int(parts[2]), int(parts[3])
        except (IndexError, ValueError):
            return "ERROR bad arguments"
        if n < 1 or lo > hi:
            return "ERROR bad range"
        box = run_in_main(lambda: generate(n, lo, hi))
        return "OK" if "error" not in box else "ERROR " + box["error"]
    if name == "MOVE":
        try:
            x, y = int(parts[1]), int(parts[2])
        except (IndexError, ValueError):
            return "ERROR bad arguments"
        run_in_main(lambda: root.geometry(f"+{x}+{y}"))
        return "OK"
    if name == "QUIT":
        root.after(100, root.destroy)
        return "OK"
    return "ERROR unknown command"

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    def serve():
        while True:
            conn, _ = server.accept()
            with conn:
                line = conn.makefile("r", encoding="utf-8").readline().strip()
                conn.sendall((handle(line) + "\n").encode("utf-8"))

    threading.Thread(target=serve, daemon=True).start()

try:
    start_server()
except OSError:
    print("Object2 вже запущений (порт зайнятий).")
    raise SystemExit

poll_tasks()
root.mainloop()