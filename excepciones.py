"""
excepciones.py
Jerarquía de excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, de modo que la aplicación puede capturar
cualquier error propio del dominio con un solo `except SoftwareFJError`.
"""


class SoftwareFJError(Exception):
    """Excepción base del sistema."""

    codigo_defecto = "FJ-000"

    def __init__(self, mensaje="Error en el sistema Software FJ", codigo=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo or self.codigo_defecto

    def __str__(self):
        return f"[{self.codigo}] {self.mensaje}"


class ParametroFaltanteError(SoftwareFJError):
    """Se omitió un parámetro obligatorio."""
    codigo_defecto = "FJ-001"


class ClienteInvalidoError(SoftwareFJError):
    """Datos de cliente inválidos o duplicados."""
    codigo_defecto = "FJ-100"


class ServicioInvalidoError(SoftwareFJError):
    """Parámetros de servicio inválidos."""
    codigo_defecto = "FJ-200"


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio existe pero no está disponible."""
    codigo_defecto = "FJ-201"


class ReservaInvalidaError(SoftwareFJError):
    """Intento de reserva incorrecto."""
    codigo_defecto = "FJ-300"


class OperacionNoPermitidaError(SoftwareFJError):
    """La operación no es válida para el estado actual del objeto."""
    codigo_defecto = "FJ-301"


class CalculoInconsistenteError(SoftwareFJError):
    """Un cálculo de costos produjo o recibió valores inconsistentes."""
    codigo_defecto = "FJ-400"
