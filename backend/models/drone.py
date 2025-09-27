class Drone:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.assigned_row = None
        self.current_position = 0  # Siempre empieza en posición 0
        self.status = "idle"  # idle, moving, irrigating, finished
    
    def assign_to_row(self, row_number):
        self.assigned_row = row_number
    
    def move_forward(self):
        self.current_position += 1
        self.status = "moving"
    
    def move_backward(self):
        self.current_position -= 1
        self.status = "moving"
    
    def irrigate(self):
        self.status = "irrigating"
    
    def wait(self):
        self.status = "waiting"
    
    def finish(self):
        self.status = "finished"
    
    def reset_position(self):
        self.current_position = 0
        self.status = "idle"
