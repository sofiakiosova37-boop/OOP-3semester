from shapes import Shape, Point, Line, Rectangle, Ellipse 

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

    def on_drag(self, event):
        if self.rubber_line_id:
            self.canvas.delete(self.rubber_line_id)
        self.rubber_line_id = Shape.draw_rubber_band(
            self.canvas, self.start_x, self.start_y, event.x, event.y
        )

    def on_release(self, event):    
        if self.rubber_line_id:
            self.canvas.delete(self.rubber_line_id)
            self.rubber_line_id = None

        shape_obj = None
        if len(self.shapes) >= self.MAX_SHAPES:
            print(f"Досягнуто ліміту об'єктів ({self.MAX_SHAPES})!")
            return
        
        if self.current_shape_type == "Point":
            shape_obj = Point(self.start_x, self.start_y)
        elif self.current_shape_type == "Line":
            shape_obj = Line(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape_type == "Rectangle":
            shape_obj = Rectangle(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape_type == "Ellipse":
            shape_obj = Ellipse(self.start_x, self.start_y, event.x, event.y)

        if shape_obj:
            shape_obj.draw(self.canvas)
            self.shapes.append(shape_obj)
            print(f"Додано об'єкт {self.current_shape_type}. Всього у масиві: {len(self.shapes)}/{self.MAX_SHAPES}")