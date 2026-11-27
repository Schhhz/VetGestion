from datetime import date, datetime
import json
from functools import reduce
class Propietario:
    def __init__(self, nombre, telefono):
        self._nombre = nombre
        self._telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @property
    def telefono(self):
        return self._telefono

class Mascota:
    def __init__(self, nombre, edad, raza, propietario):
        self._nombre = nombre
        self._edad = edad
        self._raza = raza
        self._propietario = propietario

    @property
    def nombre(self):
        return self._nombre

    @property
    def edad(self):
        return self._edad

    @property
    def raza(self):
        return self._raza

    @property
    def propietario(self):
        return self._propietario

class Veterinario:
    def __init__(self, nombre, especialidad):
        self._nombre = nombre
        self._especialidad = especialidad
        self._estado = "Disponible"

    @property
    def nombre(self):
        return self._nombre

    @property
    def especialidad(self):
        return self._especialidad
    @property
    def estado(self):
        return self._estado
    def ocupar(self):
        self._estado = "Ocupado"

    def liberar(self):
        self._estado = "Disponible"

class Cita:
    def __init__(self, mascota, veterinario, motivo, fecha, hora_llegada):
        self._mascota = mascota
        self._veterinario = veterinario
        self._motivo = motivo
        self._fecha = fecha
        self._hora_llegada = hora_llegada
        self._estado = "En espera" if veterinario is None else "En atención"

    @property
    def mascota(self):
        return self._mascota

    @property
    def veterinario(self):
        return self._veterinario

    @property
    def motivo(self):
        return self._motivo

    @property
    def fecha(self):
        return self._fecha

    @property
    def hora_llegada(self):
        return self._hora_llegada
    @property
    def estado(self):
        return self._estado
    def asignar_veterinario(self, veterinario):
        self._veterinario = veterinario
        self._estado = "En atención"

propietarios = []
mascotas = []
veterinarios = []
citas = []

def guardar_datos():
    datos = {
        "propietarios": [
            {
                "nombre": p.nombre,
                "telefono": p.telefono
            }
            for p in propietarios
        ],

        "mascotas": [
            {
                "nombre": m.nombre,
                "edad": m.edad,
                "raza": m.raza,
                "propietario": propietarios.index(m.propietario)
            }
            for m in mascotas
        ],

        "veterinarios": [
            {
                "nombre": v.nombre,
                "especialidad": v.especialidad
            }
            for v in veterinarios
        ],

        "citas": [
            {

                "mascota": mascotas.index(c.mascota),
                "veterinario": veterinarios.index(c.veterinario) if c.veterinario is not None else None,
                "motivo": c.motivo,
                "fecha": c.fecha,
                "hora_llegada": c.hora_llegada,
                "estado": c.estado
            }
            for c in citas
        ]
    }

    with open("datos_vetgestion.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def cargar_datos():
    try:
        with open("datos_vetgestion.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        for p in datos["propietarios"]:
            propietarios.append(
                Propietario(p["nombre"], p["telefono"])
            )

        for m in datos["mascotas"]:
            propietario = propietarios[m["propietario"]]

            mascotas.append(
                Mascota(m["nombre"], m["edad"], m["raza"], propietario)
            )

        for v in datos["veterinarios"]:
            veterinarios.append(
                Veterinario(v["nombre"], v["especialidad"])
            )

        for c in datos["citas"]:
            mascota = mascotas[c["mascota"]]

            veterinario = (
                veterinarios[c["veterinario"]]
                if c["veterinario"] is not None
                else None
            )

            nueva_cita = Cita(
                mascota,
                veterinario,
                c["motivo"],
                c["fecha"],
                c["hora_llegada"]
            )

            nueva_cita._estado = c.get("estado", nueva_cita.estado)
            citas.append(nueva_cita)

        # Restaurar disponibilidad de veterinarios
        for veterinario in veterinarios:
            veterinario.liberar()

        for cita in citas:
            if cita.estado == "En atención" and cita.veterinario is not None:
                cita.veterinario.ocupar()

        print("Datos anteriores cargados correctamente.")

    except FileNotFoundError:
        print("No hay datos anteriores. Se iniciará un registro nuevo.")

def registrar_veterinario():
    print("\n--- REGISTRAR VETERINARIO ---")

    nombre = input("Nombre del veterinario: ").strip()

    if not nombre or not any(c.isalpha() for c in nombre):
        print("Error: ingrese un nombre válido.")
        return

    if any(v.nombre.lower() == nombre.lower() for v in veterinarios):
        print("Error: este veterinario ya está registrado.")
        return

    especialidad = input("Especialidad: ").strip()

    if not especialidad or not any(c.isalpha() for c in especialidad):
        print("Error: ingrese una especialidad válida.")
        return
    veterinario = Veterinario(nombre, especialidad)
    veterinarios.append(veterinario)

    guardar_datos()

    print("Veterinario registrado correctamente.")

def registrar_propietario():
    print("\n--- REGISTRO DE PROPIETARIO ---")

    while True:
        nombre = input("Ingrese el nombre del propietario: ").strip()

        if nombre and all(c.isalpha() or c.isspace() or c in "-'" for c in nombre):
            break

        print("Error: ingrese un nombre válido, sin números.")
    
        while True:
            telefono = input("Ingrese el teléfono: ").strip()
            if len(telefono) == 9 and telefono.isdigit():
                break

    print("Error: el teléfono debe contener exactamente 9 dígitos.")

    nuevo_propietario = Propietario(nombre, telefono)

    propietarios.append(nuevo_propietario)
    guardar_datos()

    print("\n¡Propietario registrado correctamente!")


def registrar_mascota():
    print("\n--- REGISTRO DE MASCOTA ---")

    if not propietarios:
        print("Primero debe registrar un propietario.")
        return

    print("\nPropietarios registrados:")

    for i, propietario in enumerate(propietarios):
        print(f"{i + 1}. {propietario.nombre} - {propietario.telefono}")

    try:
        seleccion = input("Seleccione el número del propietario: ")

        if not seleccion.isdigit():
            print("Error: debe ingresar un número.")
            return
        seleccion = int(seleccion)

        if seleccion < 1 or seleccion > len(propietarios):
            print("Selección no válida.")
            return

        propietario_seleccionado = propietarios[seleccion - 1]

        while True:
            nombre = input("Nombre de la mascota: ").strip()

            if nombre and any(c.isalpha() for c in nombre):
                break

            print("Error: ingrese un nombre válido.")
        while True:
            edad = input("Edad de la mascota: ")
            if edad.isdigit():
                edad = int(edad)
                if edad <= 30:
                    break

                print("Error: ingrese una edad válida entre 0 y 30 años.")

        while True:
            raza = input("Raza de la mascota: ").strip()
            if raza:
                break

            print("Error: la raza no puede estar vacía.")

        nueva_mascota = Mascota(
            nombre, edad, raza, propietario_seleccionado
        )

        mascotas.append(nueva_mascota)
        guardar_datos()

        print("\n¡Mascota registrada correctamente!")
        print("Mascota:", nueva_mascota.nombre)
        print("Propietario:", propietario_seleccionado.nombre)

    except ValueError:
        print("Error: ingrese una edad y selección válidas.")



def registrar_cita():
    print("\n--- REGISTRO DE VISITA ---")

    if not mascotas:
        print("Primero debe registrar una mascota.")
        return

    print("\nMascotas registradas:")

    for i, mascota in enumerate(mascotas):
        print(f"{i + 1}. {mascota.nombre} - Propietario: {mascota.propietario.nombre}")

    seleccion = input("Seleccione la mascota: ")

    if not seleccion.isdigit():
        print("Error: debe ingresar un número.")
        return

    seleccion = int(seleccion)

    if seleccion < 1 or seleccion > len(mascotas):
        print("Selección no válida.")
        return

    mascota_seleccionada = mascotas[seleccion - 1]
    cita_existente = next(
        (
            c for c in citas
            if c.mascota == mascota_seleccionada
            and c.estado in ["En atención", "En espera"]
        ),
        None
    )

    if cita_existente is not None:
        print("\nEsta mascota ya tiene una visita activa.")
        print("Estado actual:", cita_existente.estado)
        return

    disponibles = [
        v for v in veterinarios
        if v.estado == "Disponible"
    ]

    veterinario_seleccionado = None

    if disponibles:
        print("\nVeterinarios disponibles:")

        for i, veterinario in enumerate(disponibles):
            print(f"{i + 1}. {veterinario.nombre} - {veterinario.especialidad}")

        seleccion_vet = input("Seleccione el veterinario: ")

        if not seleccion_vet.isdigit():
            print("Error: debe ingresar un número.")
            return

        seleccion_vet = int(seleccion_vet)

        if seleccion_vet < 1 or seleccion_vet > len(disponibles):
            print("Selección no válida.")
            return

        veterinario_seleccionado = disponibles[seleccion_vet - 1]
        veterinario_seleccionado.ocupar()

    else:
        print("\nNo hay veterinarios disponibles.")
        print("La visita quedará en espera.")

    motivo = input("Ingrese el motivo de consulta: ").strip()

    if not motivo or not any(c.isalpha() for c in motivo):
        print("Error: el motivo debe contener al menos una letra.")

        if veterinario_seleccionado is not None:
           veterinario_seleccionado.liberar()

        return

    fecha_llegada = datetime.now()
    fecha = fecha_llegada.strftime("%d/%m/%Y")
    hora_llegada = fecha_llegada.strftime("%H:%M")

    nueva_cita = Cita(
        mascota_seleccionada,
        veterinario_seleccionado,
        motivo,
        fecha,
        hora_llegada
    )

    citas.append(nueva_cita)
    guardar_datos()

    print("\n¡Visita registrada correctamente!")
    print("Mascota:", mascota_seleccionada.nombre)
    print("Fecha:", fecha)
    print("Hora de llegada:", hora_llegada)
    print("Estado:", nueva_cita.estado)

    if veterinario_seleccionado is not None:
        print("Veterinario:", veterinario_seleccionado.nombre)

def consultar_registros():
    print("\n--- CONSULTA DE REGISTROS ---")

    if not propietarios:
        print("No hay propietarios registrados.")
        return

    print("\nPropietarios registrados:")

    for i, propietario in enumerate(propietarios):
        print(f"\n{i + 1}. {propietario.nombre}")
        print(f"   Teléfono: {propietario.telefono}")

        mascotas_propietario = list(
            filter(lambda m: m.propietario == propietario, mascotas)
        )

        if not mascotas_propietario:
            print("   No tiene mascotas registradas.")
            continue

        edades = list(map(lambda m: m.edad, mascotas_propietario))
        edad_total = reduce(lambda a, b: a + b, edades, 0)

        print("   Edad acumulada de sus mascotas:", edad_total)

        for mascota in mascotas_propietario:
            print(f"\n   Mascota: {mascota.nombre}")
            print(f"   Edad: {mascota.edad}")
            print(f"   Raza: {mascota.raza}")

            historial = list(
                filter(lambda c: c.mascota == mascota, citas)
            )

            if historial:
                print("   Historial de visitas:")

                for cita in historial:
                    print(f"      Fecha: {cita.fecha}")
                    print(f"      Hora de llegada: {cita.hora_llegada}")
                    print(f"      Motivo: {cita.motivo}")
                    print(f"      Estado: {cita.estado}")
                    if cita.veterinario is not None:
                        print(f"      Veterinario: {cita.veterinario.nombre}")
                        print(f"      Especialidad: {cita.veterinario.especialidad}")
                    else:
                        print("      Veterinario: Pendiente de asignación")

            else:
                print("   Sin visitas registradas.")




def finalizar_cita():
    print("\n--- FINALIZAR VISITA ---")

    citas_activas = [
        c for c in citas
        if c.estado == "En atención"
    ]

    if not citas_activas:
        print("No hay visitas en atención.")
        return

    print("\nVisitas en atención:")

    for i, cita in enumerate(citas_activas):
        print(
            f"{i + 1}. {cita.mascota.nombre} | "
            f"Veterinario: {cita.veterinario.nombre} | "
            f"Motivo: {cita.motivo}"
        )

    seleccion = input("\nSeleccione la visita finalizada: ")

    if not seleccion.isdigit():
        print("Error: debe ingresar un número.")
        return

    seleccion = int(seleccion)

    if seleccion < 1 or seleccion > len(citas_activas):
        print("Selección no válida.")
        return

    cita_finalizada = citas_activas[seleccion - 1]
    veterinario = cita_finalizada.veterinario

    cita_finalizada._estado = "Finalizada"
    veterinario.liberar()

    print("\nVisita finalizada correctamente.")
    print("Mascota:", cita_finalizada.mascota.nombre)
    print("Veterinario:", veterinario.nombre)

    siguiente_cita = next(
        (c for c in citas if c.estado == "En espera"),
        None
    )

    if siguiente_cita is not None:
        siguiente_cita.asignar_veterinario(veterinario)
        veterinario.ocupar()

        print("\n¡Siguiente visita asignada automáticamente!")
        print("Mascota:", siguiente_cita.mascota.nombre)
        print("Veterinario:", veterinario.nombre)
    else:
        print("\nNo hay pacientes esperando.")
        print("Veterinario disponible:", veterinario.nombre)

    guardar_datos()

def eliminar_cita():
    print("\n--- ELIMINAR VISITA ---")

    if not citas:
        print("No hay visitas registradas.")
        return

    for i, cita in enumerate(citas):
        veterinario = (

            cita.veterinario.nombre
            if cita.veterinario is not None
            else "Pendiente"
        )

        print(
            f"{i + 1}. Mascota: {cita.mascota.nombre} | "
            f"Veterinario: {veterinario} | "
            f"Estado: {cita.estado} | "
            f"Fecha: {cita.fecha} | "
            f"Hora: {cita.hora_llegada} | "
            f"Motivo: {cita.motivo}"
        )

    seleccion = input("\nSeleccione la visita que desea eliminar: ")

    if not seleccion.isdigit():
        print("Error: debe ingresar un número.")
        return

    seleccion = int(seleccion)

    if seleccion < 1 or seleccion > len(citas):
        print("Selección no válida.")
        return

    eliminada = citas.pop(seleccion - 1)
    guardar_datos()

    print("\nVisita eliminada correctamente.")
    print("Mascota:", eliminada.mascota.nombre)



def eliminar_todos_los_registros():
    print("\n--- ELIMINAR TODOS LOS REGISTROS ---")
    print("Se eliminarán propietarios, mascotas, veterinarios y visitas.")

    confirmacion = input("Escriba SI para confirmar: ")

    if confirmacion == "SI":
        propietarios.clear()
        mascotas.clear()
        veterinarios.clear()
        citas.clear()

        guardar_datos()

        print("\nTodos los registros fueron eliminados.")
    else:
        print("\nOperación cancelada.")

def menu_principal():
    while True:
        print("\n===================================")
        print("             VETGESTIÓN")
        print("    Sistema de gestión veterinaria")
        print("===================================")
        print("1. Registrar propietario")
        print("2. Registrar mascota")
        print("3. Registrar veterinario")
        print("4. Registrar visita")
        print("5. Consultar registros")
        print("6. Finalizar visita")
        print("7. Eliminar una visita")
        print("8. Eliminar todos los registros")
        print("9. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            registrar_propietario()

        elif opcion == "2":
            registrar_mascota()

        elif opcion == "3":
            registrar_veterinario()

        elif opcion == "4":
            registrar_cita()

        elif opcion == "5":
            consultar_registros()

        elif opcion == "6":
            finalizar_cita()

        elif opcion == "7":
            eliminar_cita()

        elif opcion == "8":
            eliminar_todos_los_registros()

        elif opcion == "9":
            print("\nGracias por utilizar VetGestión.")
            break

        else:
            print("\nOpción no válida. Intente nuevamente.")

if __name__ == "__main__":
    cargar_datos()
    menu_principal()