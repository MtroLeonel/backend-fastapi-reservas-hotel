class HotelAPIException(Exception):
    """Clase base para excepciones de nuestra API"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        
class ResourceNotFoundException(HotelAPIException):
    """Error cuando un Hotel no existe (404)"""
    def __init__(self, message: str = "Hotel not found"):
        super().__init__(message, status_code=404)

class DuplicateHotelException(HotelAPIException):
    """Error cuando el nombre del hotel ya existe (400)"""
    def __init__(self, message: str = "Hotel name already exists"):
        super().__init__(message, status_code=400)

class BadRequestException(HotelAPIException):
    """Error genérico de solicitud inválida (400)"""
    def __init__(self, message: str = "Invalid request"):
        super().__init__(message, status_code=400)