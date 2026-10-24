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
        return canvas.create_rectangle(
            self.x1, self.y1, 
            self.x2, self.y2,
            outline="black", fill="#8BF7FF"
        )
    def draw_rubber_band(self, canvas):
        return canvas.create_rectangle(
            self.x1, self.y1, 
            self.x2, self.y2,
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

# new figures
    class line_circles(Line, Ellipse):
        def draw(self, canvas):
            Line.draw(self, canvas)
            self.x2, self.y2 = (
                self.x1,
                self.y1,
            30    )
            canvas.create_oval(
        self.x1 - 5, 
        self.y1 - 5, 
        self.x1 + 5, 
        self.y1 + 5, 
        fill="pink"
    )
            canvas.create_oval(
        self.x2 - 5, 
        self.y2 - 5, 
        self.x2 + 5, 
        self.y2 + 5, 
        fill="purple"
    )
        def draw_rubber_band(self, canvas):
            Line.draw_rubber_band(self, canvas)
            canvas.create_oval(
                self.x1 - 5,
                self.y1 - 5,
                self.x1 + 5,
                self.y1 + 5,
                outline="red",
                dash=(2, 2),
            )
            canvas.create_oval(
                self.x2 - 5,
                self.y2 - 5,
                self.x2 + 5,
                self.y2 + 5,
                outline="red",
                dash=(2, 2),
            )


    class Cube(Line, Point):
        def draw(self, canvas):
            x_min=min(self.x1, self.x2)
            x_max=max(self.x1, self.x2)
            y_min=min(self.y1, self.y2)
            y_max=max(self.y1, self.y2)
            W=x_max - x_min
            H=y_max - y_min
            S= min(W, H)
            verticles = [
            L_UP = (x_min, y_min)
            R_UP = (x_min + S, y_min)
            L_DOWN = (x_min, y_min + S)
            R_DOWN = (x_min + S, y_min + S)
            L_UP_BACK = (x_min + S*0.3, y_min - S*0.3)
            R_UP_BACK = (x_min + S*1.3+S, y_min - S*0.3)
            L_DOWN_BACK = (x_min + S*0.3, y_min + S-S*0.3)
            R_DOWN_BACK = (x_min + S*0.3+S, y_min + S-S*0.3)
            ]
        
        def draw_rubber_band(self, canvas):