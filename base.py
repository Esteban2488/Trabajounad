"""
base.py
Configuración del archivo de logs y clase abstracta general del sistema.
"""
import itertools
import logging
import os
from abc import ABC, abstractmethod

RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


def obtener_logger(nombre="software_fj"):
    """Devuelve un logger que escribe errores y eventos en logs/software_fj.log."""
    logger = logging.getLogger(nombre)
    if logger.handlers:  # evita duplicar handlers
        return logger
    logger.setLevel(logging.DEBUG)
    os.makedirs(RUTA_LOGS, exist_ok=True)
    handler = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    )
    logger.addHandler(handler)
    logger.propagate = False
    return logger


log = obtener_logger()


class Entidad(ABC):
    """
    Clase abstracta que representa cualquier entidad general del sistema
    (Cliente, Servicio, Reserva). Aporta un identificador único autogenerado
    y obliga a las subclases a implementar `describir()`.
    """

    _contador = itertools.count(1)

    def __init__(self):
        self._id = next(Entidad._contador)

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Descripción legible de la entidad."""

    def __str__(self):
        return self.describir()
