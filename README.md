# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Curso Programación (213023) – UNAD. Aplicación en Python 3, orientada a objetos,
**sin base de datos**: los datos viven en objetos y listas internas; los archivos
solo se usan para el registro de eventos y errores (`logs/software_fj.log`).

## Ejecución
```
python main.py
```
No requiere librerías externas (solo biblioteca estándar).

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas (`SoftwareFJError` y 7 derivadas) |
| `base.py` | Logger a archivo y clase abstracta `Entidad` |
| `cliente.py` | `Cliente` con encapsulación y validaciones (regex) |
| `servicios.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reserva.py` | `Reserva` y `EstadoReserva`: confirmar, cancelar, procesar |
| `gestor.py` | `GestorFJ`: listas internas y manejo centralizado de errores |
| `main.py` | Simulación de 20 operaciones válidas e inválidas |

## Requisitos de la guía y dónde se cumplen
- **Clase abstracta general**: `Entidad` (`base.py`).
- **Cliente con validaciones y encapsulación**: atributos privados + `@property` con setters validados.
- **Servicio abstracto + 3 especializados**: polimorfismo en `calcular_costo`, `describir`, `validar_parametros`.
- **Reserva** (cliente, servicio, duración, estado): `confirmar()`, `cancelar()`, `procesar()`.
- **Métodos sobrecargados**: `calcular_costo_total(horas, impuesto=None, descuento=None)`,
  `costo_con_impuesto(...)`, `costo_con_descuento(...)` (Python emula la sobrecarga con parámetros opcionales).
- **Excepciones personalizadas**: `excepciones.py`.
- **try/except**: `Servicio.calcular_costo_total`, `GestorFJ._ejecutar`.
- **try/except/else**: `GestorFJ.registrar_servicio`.
- **try/except/else/finally**: `GestorFJ.registrar_cliente`, `Reserva.procesar`.
- **Encadenamiento (`raise ... from e`)**: `Reserva.__init__`, `Reserva.procesar`,
  `Servicio.calcular_costo_total`, `GestorFJ.registrar_servicio`.
- **Log de errores y eventos**: `logs/software_fj.log` (incluye la cadena de causas).
- **≥ 10 operaciones**: 20 operaciones en `main.py`, con errores graves intercalados;
  el programa nunca se detiene.

## Notas de diseño
- El gestor devuelve `None` ante un error y lo registra, por lo que un fallo no afecta a las demás operaciones.
- Los IDs son un contador global de `Entidad`; un objeto cuya creación falla también consume un número.
