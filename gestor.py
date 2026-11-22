"""
gestor.py
GestorFJ: administra las listas internas de clientes, servicios y reservas.
Cada operación captura sus errores, los registra en el log y devuelve None,
de modo que la aplicación nunca se detiene por un fallo individual.
"""
from base import log
from cliente import Cliente
from excepciones import (ClienteInvalidoError, ServicioInvalidoError,
                         SoftwareFJError)
from reserva import Reserva
from servicios import Servicio


class GestorFJ:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    # ---- Consultas (copias para proteger el encapsulamiento) ----
    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def reservas(self):
        return list(self._reservas)

    # ---- Manejo centralizado de errores ----
    @staticmethod
    def _reportar(contexto, exc):
        log.error(f"{contexto}: {type(exc).__name__}: {exc}")
        causa = exc.__cause__
        while causa is not None:  # recorre la cadena de excepciones
            log.error(f"    causado por -> {type(causa).__name__}: {causa}")
            causa = causa.__cause__
        print(f"   ✗ Error controlado en {contexto}: {exc}")
        if exc.__cause__ is not None:
            print(f"     └─ causa: {type(exc.__cause__).__name__}: {exc.__cause__}")

    # ---- Clientes (try / except / else / finally) ----
    def registrar_cliente(self, nombre=None, documento=None, email=None, telefono=None):
        cliente = None
        try:
            cliente = Cliente(nombre, documento, email, telefono)
            if any(c.documento == cliente.documento for c in self._clientes):
                raise ClienteInvalidoError(
                    f"Ya existe un cliente con el documento {cliente.documento}")
        except SoftwareFJError as e:
            self._reportar("registrar_cliente", e)
            return None
        except Exception as e:  # error inesperado: el sistema sigue activo
            self._reportar("registrar_cliente (inesperado)", e)
            return None
        else:
            self._clientes.append(cliente)
            log.info(f"Cliente registrado: {cliente.describir()}")
            print(f"   ✓ {cliente.describir()}")
            return cliente
        finally:
            log.debug("Intento de registro de cliente finalizado")

    # ---- Servicios ----
    def registrar_servicio(self, clase, *args, **kwargs):
        try:
            if not (isinstance(clase, type) and issubclass(clase, Servicio)):
                raise ServicioInvalidoError(f"{clase!r} no es un tipo de servicio válido")
            try:
                servicio = clase(*args, **kwargs)
            except TypeError as e:  # clase abstracta o argumentos incorrectos
                raise ServicioInvalidoError(
                    f"No se pudo crear el servicio {clase.__name__}") from e
        except SoftwareFJError as e:
            self._reportar("registrar_servicio", e)
            return None
        except Exception as e:
            self._reportar("registrar_servicio (inesperado)", e)
            return None
        else:
            self._servicios.append(servicio)
            log.info(f"Servicio registrado: {servicio.describir()}")
            print(f"   ✓ {servicio.describir()}")
            return servicio

    # ---- Reservas ----
    def crear_reserva(self, cliente, servicio, horas, **opciones):
        try:
            reserva = Reserva(cliente, servicio, horas, **opciones)
        except SoftwareFJError as e:
            self._reportar("crear_reserva", e)
            return None
        except Exception as e:
            self._reportar("crear_reserva (inesperado)", e)
            return None
        self._reservas.append(reserva)
        log.info(f"Reserva creada: {reserva.describir()}")
        print(f"   ✓ {reserva.describir()}")
        return reserva

    def confirmar_reserva(self, reserva):
        return self._ejecutar("confirmar_reserva", reserva, "confirmar")

    def cancelar_reserva(self, reserva):
        return self._ejecutar("cancelar_reserva", reserva, "cancelar")

    def procesar_reserva(self, reserva, impuesto=None, descuento=None):
        return self._ejecutar("procesar_reserva", reserva, "procesar",
                              impuesto, descuento)

    def _ejecutar(self, contexto, reserva, metodo, *args):
        try:
            resultado = getattr(reserva, metodo)(*args)
        except SoftwareFJError as e:
            self._reportar(contexto, e)
            return None
        except Exception as e:  # p. ej. reserva=None -> AttributeError
            self._reportar(f"{contexto} (inesperado)", e)
            return None
        print(f"   ✓ {reserva.describir()}")
        return True if resultado is None else resultado

    # ---- Resumen ----
    def resumen(self):
        return (f"Clientes: {len(self._clientes)} | Servicios: {len(self._servicios)} | "
                f"Reservas: {len(self._reservas)}")
