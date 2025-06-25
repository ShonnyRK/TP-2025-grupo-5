class Card:
    """
    Clase que representa un Pokémon en formato Card.
    
    Esta clase actúa como un modelo de datos para transferir información
    de Pokémon entre diferentes capas de la aplicación.
    """
    
    def __init__(self, name, height, base, weight, image, types, user=None, id=None, type_images=None, is_favourite=False):
        """
        Inicializa una nueva instancia de Card.
        
        Args:
            name (str): Nombre del Pokémon
            height (str): Altura del Pokémon
            base (int): Experiencia base del Pokémon
            weight (str): Peso del Pokémon
            image (str): URL de la imagen del Pokémon
            types (list): Lista de tipos del Pokémon
            user (User, optional): Usuario asociado al Pokémon
            id (int, optional): ID del Pokémon en la API
            type_images (list, optional): URLs de las imágenes de los tipos
            is_favourite (bool, optional): Indica si el Pokémon es favorito
        """
        self.name = name  # Nombre del pokemon
        self.height = height  # ALTURA
        self.weight = weight  # PESO
        self.base = base  # NIVEL BASE
        self.image = image  # URL de la imagen
        self.user = user  # Usuario asociado (si corresponde)
        self.id = id  # ID único (si corresponde)
        self.types = types or []  # Asegura que sea una lista por defecto
        self.type_images = type_images or []
        self.is_favourite = is_favourite

    def __str__(self):
        """Representación en string del objeto Card."""
        return (f'Card(name: {self.name}, height: {self.height}, weight: {self.weight}, '
                f'base: {self.base}, image: {self.image}, user: {self.user}, id: {self.id})')

    # Método equals.
    def __eq__(self, other):
        """
        Compara dos objetos Card por igualdad.
        
        Args:
            other: Otro objeto Card para comparar
            
        Returns:
            bool: True si los objetos son iguales, False en caso contrario
        """
        if not isinstance(other, Card):
            return False
        return (self.name, self.height, self.weight, self.id) == \
               (other.name, other.height, other.weight, other.id)

    # Método hashCode.
    def __hash__(self):
        """Retorna el hash del objeto Card."""
        return hash((self.name, self.height, self.weight, self.id))

    @property
    def display_name(self):
        """Retorna el nombre del Pokémon capitalizado."""
        return self.name.title() if self.name else ''

    @property
    def types_display(self):
        """Retorna los tipos como string separados por comas."""
        return ', '.join(self.types).title() if self.types else 'Sin tipo'

    @property
    def has_types(self):
        """Retorna True si el Pokémon tiene tipos definidos."""
        return bool(self.types)

    @property
    def is_valid(self):
        """Retorna True si la Card tiene los datos mínimos requeridos."""
        return bool(self.name and self.id)
