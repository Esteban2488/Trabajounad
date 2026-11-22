"""
reserva.py
Clase Reserva: integra cliente, servicio, duración y estado.
Implementa confirmación, cancelación y procesamiento con manejo de excepciones.
"""
from enum import Enum

from base import Entidad, log
from cliente import Cliente
from excepciones import (CalculoInconsistenteError, OperacionNoPermitidaError,
                         ReservaInvalidaError, ServicioInvalidoError,
                         ServicioNoDisponibleError)
from servicios import Servicio


class EstadoReserva(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"
    FALLIDA = "FALLIDA"


class Reserva(Entidad):
    def __init__(self, cliente, servicio, horas, **opciones):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido")
        try:
            servicio.verificar_disponibilidad()
            servicio.validar_parametros(horas, **opciones)
        except (ServicioInvalidoError, ServicioNoDisponibleError) as e:
            # Encadenamiento: el error de dominio queda como causa.
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva: {e.mensaje}") from e
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._opciones = opciones
        self._estado = EstadoReserva.PENDIENTE
        self._costo_final = None

    # ---- Encapsulación ----
    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def horas(self):
        return self._horas

    @property
    def estado(self):
        return self._estado

    @property
    def costo_final(self):
        return self._costo_final

    # ---- Operaciones ----
    def confirmar(self):
        if self._estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado.value}")
        self._estado = EstadoReserva.CONFIRMADA
        log.info(f"Reserva #{self.id} CONFIRMADA ({self._cliente.nombre} - {self._servicio.nombre})")

    def cancelar(self):
        if self._estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado.value}")
        self._estado = EstadoReserva.CANCELADA
        log.info(f"Reserva #{self.id} CANCELADA")

    def procesar(self, impuesto=None, descuento=None):
        """Calcula el costo final. Requiere que la reserva esté CONFIRMADA."""
        if self._estado is not EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas CONFIRMADAS (actual: {self._estado.value})")
        try:
            costo = self._servicio.calcular_costo_total(
                self._horas, impuesto, descuento, **self._opciones)
        except CalculoInconsistenteError as e:
            self._estado = EstadoReserva.FALLIDA
            raise ReservaInvalidaError(
                f"Falló el procesamiento de la reserva #{self.id}") from e
        else:
            self._costo_final = costo
            self._estado = EstadoReserva.PROCESADA
            log.info(f"Reserva #{self.id} PROCESADA. Costo final: ${costo:,.2f}")
            return costo
        finally:
            log.debug(f"Fin del intento de procesamiento de la reserva #{self.id} "
                      f"(estado: {self._estado.value})")

    def describir(self):
        costo = f"${self._costo_final:,.2f}" if self._costo_final is not None else "N/A"
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas}h | {self._estado.value} | Costo: {costo}")
