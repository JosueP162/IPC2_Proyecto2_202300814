class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def enqueue(self, data):
        """Agregar elemento al final de la cola"""
        new_node = QueueNode(data)
        
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        
        self.size += 1
    
    def dequeue(self):
        """Eliminar y retornar elemento del frente"""
        if self.is_empty():
            raise Exception("Cola vacía")
        
        data = self.front.data
        self.front = self.front.next
        
        if self.front is None:  # Cola quedó vacía
            self.rear = None
            
        self.size -= 1
        return data
    
    def peek(self):
        """Ver elemento del frente sin eliminarlo"""
        if self.is_empty():
            return None
        return self.front.data
    
    def is_empty(self):
        return self.front is None
    
    def get_size(self):
        return self.size
    
    def to_string(self):
        """Para debugging"""
        if self.is_empty():
            return "Cola vacía"
        
        result = "Front -> "
        current = self.front
        while current:
            result += str(current.data)
            if current.next:
                result += " -> "
            current = current.next
        result += " <- Rear"
        return result