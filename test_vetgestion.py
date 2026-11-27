import unittest
import VeterinariaLimaVet
class TestVetGestion(unittest.TestCase):
    def test_crear_propietario(self):
        propietario = VeterinariaLimaVet.Propietario(
            "Juan Perez",
            "987654321"
        )

        self.assertEqual(propietario.nombre, "Juan Perez")
        self.assertEqual(propietario.telefono, "987654321")
    def test_crear_mascota(self):
        propietario = VeterinariaLimaVet.Propietario(
            "Juan Perez",
            "987654321"
        )

        mascota = VeterinariaLimaVet.Mascota(
            "Rocky",
            4,
            "Labrador",
            propietario
        )

        self.assertEqual(mascota.nombre, "Rocky")
        self.assertEqual(mascota.edad, 4)
        self.assertEqual(mascota.raza, "Labrador")
        self.assertEqual(mascota.propietario, propietario)
    def test_crear_veterinario(self):
        veterinario = VeterinariaLimaVet.Veterinario(
            "Carlos Ramirez",
            "Medicina general"
        )

        self.assertEqual(veterinario.nombre, "Carlos Ramirez")
        self.assertEqual(veterinario.especialidad, "Medicina general")
        self.assertEqual(veterinario.estado, "Disponible")
    def test_estado_veterinario(self):
        veterinario = VeterinariaLimaVet.Veterinario(
            "Carlos Ramirez",
            "Medicina general"
        )

        veterinario.ocupar()
        self.assertEqual(veterinario.estado, "Ocupado")

        veterinario.liberar()
        self.assertEqual(veterinario.estado, "Disponible")
    def test_crear_cita(self):
        propietario = VeterinariaLimaVet.Propietario(
            "Juan Perez",
            "987654321"
        )

        mascota = VeterinariaLimaVet.Mascota(
            "Rocky",
            4,
            "Labrador",
            propietario
        )

        veterinario = VeterinariaLimaVet.Veterinario(
            "Carlos Ramirez",
            "Medicina general"
        )

        cita = VeterinariaLimaVet.Cita(
            mascota,
            veterinario,
            "Chequeo general",
            "24/11/2026",
            "10:30"
        )

        self.assertEqual(cita.mascota, mascota)
        self.assertEqual(cita.veterinario, veterinario)
        self.assertEqual(cita.motivo, "Chequeo general")
        self.assertEqual(cita.estado, "En atención")
    def test_cita_en_espera(self):
        propietario = VeterinariaLimaVet.Propietario(
            "Maria Lopez",
            "987654321"
        )

        mascota = VeterinariaLimaVet.Mascota(
            "Luna",
            3,
            "Golden Retriever",
            propietario
        )

        cita = VeterinariaLimaVet.Cita(
            mascota,
            None,
            "Control médico",
            "24/11/2026",
            "10:45"
        )

        self.assertIsNone(cita.veterinario)
        self.assertEqual(cita.estado, "En espera")
    def test_asignar_veterinario(self):
        propietario = VeterinariaLimaVet.Propietario(
            "Maria Lopez",
            "987654321"
        )

        mascota = VeterinariaLimaVet.Mascota(
            "Luna",
            3,
            "Golden Retriever",
            propietario
        )

        veterinario = VeterinariaLimaVet.Veterinario(
            "Carlos Ramirez",
            "Medicina general"
        )

        cita = VeterinariaLimaVet.Cita(
            mascota,
            None,
            "Control médico",
            "24/11/2026",
            "10:45"
        )

        cita.asignar_veterinario(veterinario)

        self.assertEqual(cita.veterinario, veterinario)
        self.assertEqual(cita.estado, "En atención")
    def test_fecha_hora_cita(self):
        propietario = VeterinariaLimaVet.Propietario(
            "Juan Perez",
            "987654321"
        )

        mascota = VeterinariaLimaVet.Mascota(
            "Rocky",
            4,
            "Labrador",
            propietario
        )

        cita = VeterinariaLimaVet.Cita(
            mascota,
            None,
            "Chequeo general",
            "24/11/2026",
            "10:30"
        )

        self.assertEqual(cita.fecha, "24/11/2026")
        self.assertEqual(cita.hora_llegada, "10:30")


if __name__ == "__main__":
    unittest.main()