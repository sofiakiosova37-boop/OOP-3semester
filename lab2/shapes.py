from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, x1, y1, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @abstractmethod
    def draw(self, canvas):
        pass

    @staticmethod
    def draw_rubber_band(canvas, x1, y1, x2, y2):
        return canvas.create_line(x1, y1, x2, y2, fill="red")

class Point(Shape):
    def draw(self, canvas):
        return canvas.create_oval(self.x1 - 2, self.y1 - 2, self.x1 + 2, self.y1 + 2, fill="black")

class Line(Shape):
    def draw(self, canvas):
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill="black")

class Rectangle(Shape):
    def draw(self, canvas):
        dx = abs(self.x2 - self.x1)
        dy = abs(self.y2 - self.y1)
        return canvas.create_rectangle(
            self.x1 - dx, self.y1 - dy, 
            self.x1 + dx, self.y1 + dy, 
            outline="black", fill="#90EE90"
        )

class Ellipse(Shape):
    def draw(self, canvas):
        return canvas.create_oval(
            self.x1, self.y1,
            self.x2, self.y2,
            outline="black", fill="#FFFB01"
        )

