from .simple_list import SimpleList

class ListOfLists:
    """
    Estructura para manejar el timeline de la simulación
    Cada índice representa un segundo, y contiene una lista de acciones
    """
    
    def __init__(self):
        self.main_list = SimpleList()  # Lista principal de segundos
        self.max_seconds = 0
    
    def add_second(self, second):
        """Agregar un nuevo segundo al timeline"""
        # Expandir si es necesario
        while self.main_list.get_size() <= second:
            self.main_list.add(SimpleList())  # Nueva lista para este segundo
        
        if second > self.max_seconds:
            self.max_seconds = second
    
    def add_action_to_second(self, second, action):
        """Agregar una acción a un segundo específico"""
        self.add_second(second)  # Asegurar que el segundo existe
        actions_list = self.main_list.get(second)
        actions_list.add(action)
    
    def get_actions_at_second(self, second):
        """Obtener todas las acciones de un segundo específico"""
        if second >= self.main_list.get_size():
            return SimpleList()  # Lista vacía si no existe
        return self.main_list.get(second)
    
    def get_max_seconds(self):
        """Obtener el número máximo de segundos simulados"""
        return self.max_seconds
    
    def is_empty(self):
        return self.main_list.is_empty()
    
    def to_string(self):
        """Para debugging - mostrar toda la simulación"""
        result = "=== TIMELINE DE SIMULACIÓN ===\n"
        
        for second in range(self.main_list.get_size()):
            actions = self.main_list.get(second)
            if not actions.is_empty():
                result += f"Segundo {second}: "
                result += actions.to_string()
                result += "\n"
        
        return result