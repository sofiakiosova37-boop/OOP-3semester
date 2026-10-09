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

    @abstractmethod
    def draw_rubber_band(self, canvas):
        pass

class Point(Shape):
    def draw(self, canvas):
        return canvas.create_oval(self.x1 - 2, self.y1 - 2, self.x1 + 2, self.y1 + 2, fill="black")
    def draw_rubber_band(self, canvas):
        return canvas.create_ovalself(self.x1 - 2, self.y1 - 2, self.x1 + 2, self.y1 + 2, fill="red")

class Line(Shape):
    def draw(self, canvas):
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill="blue")
    def draw_rubber_band(self, canvas):
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill="red", dash=(4, 2))

class Rectangle(Shape):
    def draw(self, canvas):
        width = abs(self.x2-self.x1)
        height=abs(self.y2-self.y1)
        left=((self.x1+self.x2)-(width))/2
        right=((self.x1+self.x2)+(width))/2
        top=((self.y1+self.y2)-(height))/2
        bottom=((self.y1+self.y2)+(height))/2
        return canvas.create_rectangle(
            left, top, 
            right, bottom,
            outline="black", fill="#8BF7FF"
        )
    def draw_rubber_band(self, canvas):
        width = abs(self.x2-self.x1)
        height=abs(self.y2-self.y1)
        left=((self.x1+self.x2)-(width))/2
        right=((self.x1+self.x2)+(width))/2
        top=((self.y1+self.y2)-(height))/2
        bottom=((self.y1+self.y2)+(height))/2
        return canvas.create_rectangle(
            left, top, 
            right, bottom,
            outline="black", fill="#8BF7FF"
        )

class Ellipse(Shape):
    def draw(self, canvas):
        rx = abs(self.x2 - self.x1)
        ry = abs(self.y2 - self.y1)
        left = self.x1 - rx
        top = self.y1 - ry
        right = self.x1 + rx
        bottom = self.y1 + ry
        return canvas.create_oval(
            left, top,
            right, bottom, 
            outline="black", fill="#72FF8C"
        )

    def draw_rubber_band(self, canvas):
        rx = abs(self.x2 - self.x1)
        ry = abs(self.y2 - self.y1)
        left = self.x1 - rx
        top = self.y1 - ry
        right = self.x1 + rx
        bottom = self.y1 + ry
        return canvas.create_oval(
            left, top,
            right, bottom,
            outline="red", dash=(4, 2)
        )