"""Object3 рахує детермінант квадратної матриці, яка знаходиться в буфері обміну."""
import queue
import socket
import threading
import tkinter as tk
#from fractions import Fraction
import pyperclip 

HOST = "127.0.0.1"
PORT = 50003  

root = tk.Tk()
root.title("Object3")
root.geometry("+420+420")

info_label = tk.Label(root, text="Очікування даних...", font=("Arial", 11))
info_label.pack(padx=30, pady=(15, 5))
result_label = tk.Label(root, text="", font=("Arial", 20, "bold"))
result_label.pack(padx=30, pady=(5, 20))

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

'''
def determinant(m):
    n = len(m)
    a = [[Fraction(x) for x in row] for row in m]
    det = Fraction(1)
    for i in range(n):
        p = next((r for r in range(i, n) if a[r][i] != 0), None)
        if p is None:
            return 0
        if p != i:
            a[i], a[p] = a[p], a[i]
            det = -det
        det *= a[i][i]
        for r in range(i + 1, n):
            f = a[r][i] / a[i][i]
            for c in range(i, n):
                a[r][c] -= f * a[i][c]
    return int(det)
'''
def determinant(m):
    n = len(m)
    a = [row[:] for row in m]
    sign, prev = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            for i in range(k + 1, n):
                if a[i][k] != 0:
                    a[k], a[i] = a[i], a[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
        prev = a[k][k]
    return sign * a[n - 1][n - 1]

def compute():
    text = pyperclip.paste()
    matrix = [[int(x) for x in line.split()] for line in text.strip().splitlines() if line.strip()]
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("non-square matrix or empty input")
    d = determinant(matrix)
    info_label.config(text=f" Determinant of {n}x{n}:")
    result_label.config(text=str(d))

def handle(command):
    parts = command.split()
    if not parts:
        return "ERROR empty"
    name = parts[0]

    if name == "PING":
        return "OK"
    if name == "COMPUTE":
        box = run_in_main(compute)
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
    print("Object3 is already running (port is in use).")
    raise SystemExit

poll_tasks()
root.mainloop()