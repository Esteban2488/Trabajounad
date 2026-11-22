"""
cliente.py
Clase Cliente con encapsulación de datos personales y validaciones estrictas.
"""
import re

from base import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError


class Cliente(Entidad):
    _RE_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?: [A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$")
    _RE_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
    _RE_DOCUMENTO = re.compile(r"^\d{6,12}$")
    _RE_TELEFONO = re.compile(r"^3\d{9}$")  # celular colombiano

    def __init__(self, nombre=None, documento=None, email=None, telefono=None):
        super().__init__()
        faltantes = [
            n for n, v in (("nombre", nombre), ("documento", documento),
                           ("email", email), ("telefono", telefono)) if v is None
        ]
        if faltantes:
            raise ParametroFaltanteError(
                f"Faltan parámetros obligatorios del cliente: {', '.join(faltantes)}"
            )
        # Se asigna mediante las propiedades para ejecutar las validaciones.
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    # ---- Propiedades (datos personales encapsulados) ----
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3 \
                or not self._RE_NOMBRE.match(valor.strip()):
            raise ClienteInvalidoError(
                f"Nombre inválido: {valor!r} (solo letras, mínimo 3 caracteres)")
        self._nombre = valor.strip().title()

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        if not isinstance(valor, str) or not self._RE_DOCUMENTO.match(valor):
            raise ClienteInvalidoError(
                f"Documento inválido: {valor!r} (6 a 12 dígitos numéricos)")
        self._documento = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or not self._RE_EMAIL.match(valor):
            raise ClienteInvalidoError(f"Correo electrónico inválido: {valor!r}")
        self._email = valor.lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not self._RE_TELEFONO.match(valor):
            raise ClienteInvalidoError(
                f"Teléfono inválido: {valor!r} (10 dígitos, inicia en 3)")
        self._telefono = valor

    def describir(self):
        return (f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | "
                f"{self.email} | Tel: {self.telefono}")
