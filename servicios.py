"""
servicios.py
Clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.

Polimorfismo: cada servicio sobrescribe calcular_costo(), describir() y
validar_parametros().

Sobrecarga: Python no soporta sobrecarga nativa, por lo que se emula con
parámetros opcionales (calcular_costo_total) y variantes con nombre
(costo_con_impuesto, costo_con_descuento) que delegan en el mismo cálculo.
"""
from abc import ABC, abstractmethod

from base import Entidad
from excepciones import (CalculoInconsistenteError, ServicioInvalidoError,
                         ServicioNoDisponibleError)


class Servicio(Entidad, ABC):
    IVA = 0.19

    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio es obligatorio")
        if isinstance(tarifa_hora, bool) or not isinstance(tarifa_hora, (int, float)) \
                or tarifa_hora <= 0:
            raise ServicioInvalidoError(
                f"Tarifa por hora inválida: {tarifa_hora!r} (debe ser un número > 0)")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    # ---- Encapsulación ----
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    # ---- Métodos abstractos (polimorfismo) ----
    @abstractmethod
    def calcular_costo(self, horas, **opciones):
        """Costo base del servicio, sin impuestos ni descuentos."""

    @abstractmethod
    def validar_parametros(self, horas, **opciones):
        """Lanza ServicioInvalidoError si los parámetros no son válidos."""

    @abstractmethod
    def describir(self):
        """Descripción del servicio."""

    # ---- Utilidades comunes ----
    def _validar_horas(self, horas, maximo):
        if isinstance(horas, bool) or not isinstance(horas, (int, float)):
            raise ServicioInvalidoError(f"La duración debe ser numérica: {horas!r}")
        if horas <= 0:
            raise ServicioInvalidoError(f"La duración debe ser mayor a 0: {horas}")
        if horas > maximo:
            raise ServicioInvalidoError(
                f"La duración {horas}h excede el máximo permitido ({maximo}h)")

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' no está disponible actualmente")

    # ---- Métodos "sobrecargados" ----
    def calcular_costo_total(self, horas, impuesto=None, descuento=None, **opciones):
        """
        Variantes:
          calcular_costo_total(h)                    -> costo base
          calcular_costo_total(h, impuesto)          -> base + impuesto
          calcular_costo_total(h, descuento=d)       -> base - descuento
          calcular_costo_total(h, impuesto, descuento)-> descuento y luego impuesto
        """
        try:
            self.validar_parametros(horas, **opciones)
            base = self.calcular_costo(horas, **opciones)
            total = base
            if descuento is not None:
                if not 0 <= descuento < 1:
                    raise CalculoInconsistenteError(
                        f"Descuento fuera de rango [0,1): {descuento}")
                total -= base * descuento
            if impuesto is not None:
                if not 0 <= impuesto <= 1:
                    raise CalculoInconsistenteError(
                        f"Impuesto fuera de rango [0,1]: {impuesto}")
                total *= (1 + impuesto)
            if total < 0:
                raise CalculoInconsistenteError(f"Costo negativo calculado: {total}")
            return round(total, 2)
        except (TypeError, ArithmeticError) as e:
            # Encadenamiento de excepciones: se conserva la causa original.
            raise CalculoInconsistenteError(
                "No fue posible calcular el costo con los valores dados") from e

    def costo_con_impuesto(self, horas, impuesto=None, **opciones):
        return self.calcular_costo_total(
            horas, impuesto=self.IVA if impuesto is None else impuesto, **opciones)

    def costo_con_descuento(self, horas, descuento, **opciones):
        return self.calcular_costo_total(horas, descuento=descuento, **opciones)


class ReservaSala(Servicio):
    RECARGO_PROYECTOR = 15000  # por hora

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad

    @property
    def capacidad(self):
        return self._capacidad

    def validar_parametros(self, horas, asistentes=1, proyector=False, **_):
        self._validar_horas(horas, maximo=12)
        if not isinstance(asistentes, int) or asistentes < 1:
            raise ServicioInvalidoError(f"Número de asistentes inválido: {asistentes!r}")
        if asistentes > self._capacidad:
            raise ServicioInvalidoError(
                f"{asistentes} asistentes exceden la capacidad de la sala ({self._capacidad})")

    def calcular_costo(self, horas, asistentes=1, proyector=False, **_):
        costo = horas * self.tarifa_hora
        if proyector:
            costo += horas * self.RECARGO_PROYECTOR
        return costo

    def describir(self):
        return (f"Sala '{self.nombre}' | capacidad {self._capacidad} | "
                f"${self.tarifa_hora:,.0f}/h | "
                f"{'disponible' if self.disponible else 'NO disponible'}")


class AlquilerEquipo(Servicio):
    RECARGO_SEGURO = 0.10

    def __init__(self, nombre, tarifa_hora, tipo_equipo, stock, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("El tipo de equipo es obligatorio")
        if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
            raise ServicioInvalidoError(f"Stock inválido: {stock!r}")
        self._tipo_equipo = tipo_equipo.strip()
        self._stock = stock

    @property
    def tipo_equipo(self):
        return self._tipo_equipo

    @property
    def stock(self):
        return self._stock

    def validar_parametros(self, horas, cantidad=1, seguro=False, **_):
        self._validar_horas(horas, maximo=72)
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 1:
            raise ServicioInvalidoError(f"Cantidad inválida: {cantidad!r}")
        if cantidad > self._stock:
            raise ServicioInvalidoError(
                f"Se piden {cantidad} unidades pero solo hay {self._stock} en stock")

    def calcular_costo(self, horas, cantidad=1, seguro=False, **_):
        costo = horas * self.tarifa_hora * cantidad
        if seguro:
            costo *= (1 + self.RECARGO_SEGURO)
        return costo

    def describir(self):
        return (f"Equipo '{self.nombre}' ({self._tipo_equipo}) | stock {self._stock} | "
                f"${self.tarifa_hora:,.0f}/h | "
                f"{'disponible' if self.disponible else 'NO disponible'}")


class AsesoriaEspecializada(Servicio):
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}
    RECARGO_PRESENCIAL = 20000  # tarifa fija

    def __init__(self, nombre, tarifa_hora, especialidad, nivel, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La especialidad es obligatoria")
        if not isinstance(nivel, str) or nivel.lower() not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel inválido: {nivel!r} (válidos: {', '.join(self.NIVELES)})")
        self._especialidad = especialidad.strip()
        self._nivel = nivel.lower()

    @property
    def especialidad(self):
        return self._especialidad

    @property
    def nivel(self):
        return self._nivel

    def validar_parametros(self, horas, modalidad="virtual", **_):
        self._validar_horas(horas, maximo=8)
        if modalidad not in ("virtual", "presencial"):
            raise ServicioInvalidoError(f"Modalidad inválida: {modalidad!r}")

    def calcular_costo(self, horas, modalidad="virtual", **_):
        costo = horas * self.tarifa_hora * self.NIVELES[self._nivel]
        if modalidad == "presencial":
            costo += self.RECARGO_PRESENCIAL
        return costo

    def describir(self):
        return (f"Asesoría '{self.nombre}' ({self._especialidad}, nivel {self._nivel}) | "
                f"${self.tarifa_hora:,.0f}/h | "
                f"{'disponible' if self.disponible else 'NO disponible'}")
