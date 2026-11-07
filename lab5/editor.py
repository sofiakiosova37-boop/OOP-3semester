
from shapes import Shape, Point, Line, Rectangle, Ellipse, line_circles, Cube



class Editor():
    def __init__(self, canvas):
        self.canvas = canvas
        self.MAX_SHAPES = 114 
        self.shapes = []
        self.current_shape_type = "Rectangle"

        self.start_x = 0
        self.start_y = 0
        self.rubber_line_id = None
        self.is_drawing = False
        #self.highlight_id = None   # рамка виділеного об'єкта
    
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

    def _clear_rubber_band(self):
        if self.rubber_line_id:
            if isinstance(self.rubber_line_id, (list, tuple)):
                for item_id in self.rubber_line_id:
                    self.canvas.delete(item_id)
            else:
                self.canvas.delete(self.rubber_line_id)
            self.rubber_line_id = None 

    def set_shape_type(self, shape_type):
        self.current_shape_type = shape_type
        self.is_drawing = False
        self.start_x = 0
        self.start_y = 0
        self._clear_rubber_band()

    def on_press(self, event):
        self.is_drawing = True
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if not self.is_drawing: 
            return
        if self.rubber_line_id:
            if isinstance(self.rubber_line_id, (list, tuple)):
                for item_id in self.rubber_line_id:
                    self.canvas.delete(item_id)
            else:
                self.canvas.delete(self.rubber_line_id)
            self.rubber_line_id = None

        
        #self._clear_rubber_band()
        #temp_shape = None
        #if self.current_shape_type == "Point":
         #   temp_shape = Point(self.start_x, self.start_y, event.x, event.y)
        #if temp_shape:
        #    self.rubber_line_id = temp_shape.draw_rubber_band(self.canvas)
        #if self.rubber_line_id:
        #   self.canvas.delete(self.rubber_line_id)

        temp_shape = None
        if self.current_shape_type == "Point":
            temp_shape = Point(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape_type == "Line":
            temp_shape = Line(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape_type == "Rectangle":
            temp_shape = Rectangle(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape_type == "Ellipse":
            temp_shape = Ellipse(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape_type == "line_circles":
            temp_shape = line_circles(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape_type == "Cube":
            temp_shape = Cube(self.start_x, self.start_y, event.x, event.y)

        if temp_shape:
            self.rubber_line_id = temp_shape.draw_rubber_band(self.canvas)

    def on_release(self, event): 
        if not self.is_drawing:
            return   
        self.is_drawing = False
       # self._clear_rubber_band()
        if self.rubber_line_id:
            if isinstance(self.rubber_line_id, (list, tuple)):
                for item_id in self.rubber_line_id:
                    self.canvas.delete(item_id)
            else:
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
        elif self.current_shape_type == "line_circles":
            shape_obj = line_circles(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape_type == "Cube":
            shape_obj = Cube(self.start_x, self.start_y, event.x, event.y)

        if shape_obj:
            shape_obj.draw(self.canvas)
            self.shapes.append(shape_obj)
            print(f"Додано об'єкт {self.current_shape_type}. Всього у масиві: {len(self.shapes)}/{self.MAX_SHAPES}")
            # if self.table:              # оновити таблицю
              #  self.table.refresh()

    """def save_csv(self, path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for s in self.shapes:
                writer.writerow([type(s).__name__, s.x1, s.y1, s.x2, s.y2])

    def load_csv(self, path):
        self.shapes = []
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                if len(row) != 5 or row[0] not in shape_classes:
                    continue
                shape = shape_classes[row[0]](int(row[1]), int(row[2]), int(row[3]), int(row[4]))
                self.shapes.append(shape)
        self.redraw()
"""
    def redraw(self):
        self.canvas.delete("all") 
        for s in self.shapes:
            s.draw(self.canvas)
        # if self.table:
         #   self.table.refresh()
"""
    def clear_highlight(self):
        if self.highlight_id:
            self.canvas.delete(self.highlight_id)
            self.highlight_id = None

    def highlight_shape(self, index):
        self.clear_highlight()
        if index < 0 or index >= len(self.shapes):
            return
        before = set(self.canvas.find_all())
        self.shapes[index].draw(self.canvas)
        new_ids = [i for i in self.canvas.find_all() if i not in before]
        if not new_ids:
            return
        x1, y1, x2, y2 = self.canvas.bbox(*new_ids)
        self.canvas.delete(*new_ids)
        self.highlight_id = self.canvas.create_rectangle(
            x1 - 4, y1 - 4, x2 + 4, y2 + 4,
            outline="red", width=2, dash=(4, 2))

    def delete_shape(self, index):
        if 0 <= index < len(self.shapes):
            del self.shapes[index]
            self.redraw()     
    """
_global_editor = None
def init_global_editor(canvas):
    global _global_editor
    if _global_editor is None:
        _global_editor = Editor(canvas)
    return _global_editor
def get_editor():
    return _global_editor    