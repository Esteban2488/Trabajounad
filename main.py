"""
main.py
Simulación de 20 operaciones del sistema Software FJ (válidas e inválidas).
Ejecutar:  python main.py
"""
from base import ARCHIVO_LOG, Entidad, log
from gestor import GestorFJ
from servicios import (AlquilerEquipo, AsesoriaEspecializada, ReservaSala,
                       Servicio)


def titulo(n, texto):
    print(f"\n[{n:02d}] {texto}")
    log.info(f"--- Operación {n:02d}: {texto} ---")


def main():
    log.info("========== INICIO DE LA SIMULACIÓN SOFTWARE FJ ==========")
    g = GestorFJ()

    # ---------------- CLIENTES ----------------
    titulo(1, "Registro VÁLIDO de cliente (Ana)")
    ana = g.registrar_cliente("ana maría gómez", "1012345678", "ana@correo.com", "3101234567")

    titulo(2, "Registro INVÁLIDO: correo mal formado")
    g.registrar_cliente("Pedro Ruiz", "79456123", "pedro-correo.com", "3209876543")

    titulo(3, "Registro INVÁLIDO: parámetro faltante (sin documento)")
    g.registrar_cliente(nombre="Luis Mora", email="luis@correo.com", telefono="3001112233")

    titulo(4, "Registro VÁLIDO de cliente (Carlos)")
    carlos = g.registrar_cliente("Carlos Pérez", "80123456", "carlos@empresa.co", "3156667788")

    titulo(5, "Registro INVÁLIDO: documento duplicado")
    g.registrar_cliente("Otra Persona", "1012345678", "otra@correo.com", "3112223344")

    # ---------------- SERVICIOS ----------------
    titulo(6, "Creación CORRECTA de servicios (sala, equipo, asesoría)")
    sala = g.registrar_servicio(ReservaSala, "Sala Innovación", 50000, 10)
    equipo = g.registrar_servicio(AlquilerEquipo, "Portátil Pro", 8000, "Computador", 5)
    asesoria = g.registrar_servicio(AsesoriaEspecializada, "Asesoría Cloud", 90000,
                                    "Arquitectura Cloud", "senior")

    titulo(7, "Creación INCORRECTA: tarifa negativa")
    g.registrar_servicio(AlquilerEquipo, "Proyector", -5000, "Video", 2)

    titulo(8, "Creación INCORRECTA: nivel de asesoría inexistente")
    g.registrar_servicio(AsesoriaEspecializada, "Asesoría X", 70000, "Datos", "maestro")

    titulo(9, "Creación INCORRECTA: instanciar la clase abstracta Servicio")
    g.registrar_servicio(Servicio, "Genérico", 1000)

    # ---------------- RESERVAS ----------------
    titulo(10, "Reserva EXITOSA: sala con proyector -> confirmar -> procesar (IVA + descuento)")
    r1 = g.crear_reserva(ana, sala, 3, asistentes=8, proyector=True)
    g.confirmar_reserva(r1)
    g.procesar_reserva(r1, impuesto=0.19, descuento=0.10)

    titulo(11, "Reserva FALLIDA: asistentes exceden la capacidad de la sala")
    g.crear_reserva(carlos, sala, 2, asistentes=25)

    titulo(12, "Reserva FALLIDA: servicio no disponible")
    equipo_fuera = g.registrar_servicio(AlquilerEquipo, "Cámara 4K", 12000, "Video", 3,
                                        disponible=False)
    g.crear_reserva(carlos, equipo_fuera, 4)

    titulo(13, "Operación NO PERMITIDA: confirmar dos veces la misma reserva")
    g.confirmar_reserva(r1)

    titulo(14, "Reserva EXITOSA con cancelación; luego intentar procesarla (no permitido)")
    r2 = g.crear_reserva(carlos, asesoria, 2, modalidad="presencial")
    g.cancelar_reserva(r2)
    g.procesar_reserva(r2)

    titulo(15, "Cálculo INCONSISTENTE: descuento inválido (texto) -> excepción encadenada")
    r3 = g.crear_reserva(ana, equipo, 24, cantidad=2, seguro=True)
    g.confirmar_reserva(r3)
    g.procesar_reserva(r3, impuesto=0.19, descuento="diez")

    titulo(16, "Reserva FALLIDA: cantidad de equipos mayor al stock")
    g.crear_reserva(ana, equipo, 5, cantidad=50)

    titulo(17, "Reserva FALLIDA: duración inválida (negativa)")
    g.crear_reserva(carlos, sala, -2)

    titulo(18, "Reserva FALLIDA: cliente None (dato faltante)")
    g.crear_reserva(None, sala, 2)

    titulo(19, "Reserva EXITOSA de equipo con seguro e IVA")
    r4 = g.crear_reserva(carlos, equipo, 10, cantidad=3, seguro=True)
    g.confirmar_reserva(r4)
    g.procesar_reserva(r4, impuesto=0.19)

    titulo(20, "Sistema sigue activo: reserva de asesoría exitosa tras todos los errores")
    r5 = g.crear_reserva(ana, asesoria, 4, modalidad="virtual")
    g.confirmar_reserva(r5)
    g.procesar_reserva(r5, descuento=0.05)

    # ---------------- POLIMORFISMO ----------------
    print("\n=== Demostración de polimorfismo: costo de 2 horas en cada servicio ===")
    for s in g.servicios:
        try:
            print(f"   {s.nombre:<18} base=${s.calcular_costo_total(2):>10,.2f}  "
                  f"con IVA=${s.costo_con_impuesto(2):>10,.2f}  "
                  f"con 15% desc=${s.costo_con_descuento(2, 0.15):>10,.2f}")
        except Exception as e:  # nunca debe detener la demostración
            log.error(f"Demostración polimórfica: {e}")

    print("\n=== Resumen final ===")
    print("  ", g.resumen())
    for r in g.reservas:
        print("  ", r.describir())
    print(f"\nLog de eventos y errores en: {ARCHIVO_LOG}")
    log.info("========== FIN DE LA SIMULACIÓN (sin interrupciones) ==========")


if __name__ == "__main__":
    main()
