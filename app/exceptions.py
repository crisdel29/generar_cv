# app/exceptions.py
class CVSystemException(Exception):
    """Excepción base para el sistema"""
    pass

class DatabaseError(CVSystemException):
    """Errores relacionados con la base de datos"""
    pass

class ValidationError(CVSystemException):
    """Errores de validación de datos"""
    pass

class TemplateError(CVSystemException):
    """Errores relacionados con las plantillas"""
    pass