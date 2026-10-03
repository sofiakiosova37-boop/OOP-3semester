import lab2.shapes as shapes
from lab2.shapes import Shape, Point, Line, Rectangle, Ellipse 

class Editor():
    def __init__(self, canvas):
        self.canvas = canvas
        self.MAX_SHAPES = 113 
        self.shapes = []
        self.current_shape_type = "Rectangle"

        self.start_x = 0
        self.start_y = 0
        self.rubber_line_id = None

        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

    def set_shape_type(self, shape_type):
        self.current_shape_type = shape_type

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        