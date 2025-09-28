class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SimpleList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def add(self, data):
        """Agregar elemento al final"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def get(self, index):
        """Obtener elemento por índice"""
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        
        current = self.head
        for i in range(index):
            current = current.next
        return current.data
    
    def remove(self, index):
        """Eliminar elemento por índice"""
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        
        if index == 0:
            self.head = self.head.next
        else:
            current = self.head
            for i in range(index - 1):
                current = current.next
            current.next = current.next.next
        
        self.size -= 1
    
    def find(self, data):
        """Encontrar índice de un elemento"""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1
    
    def is_empty(self):
        return self.size == 0
    
    def get_size(self):
        return self.size
    
    def to_string(self):
        """Para debugging"""
        result = "["
        current = self.head
        while current:
            result += str(current.data)
            if current.next:
                result += ", "
            current = current.next
        result += "]"
        return result
    