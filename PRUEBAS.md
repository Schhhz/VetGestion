\# Pruebas automatizadas de VetGestión



\## Objetivo



Verificar el funcionamiento de las principales clases y métodos del sistema mediante pruebas unitarias con la biblioteca unittest de Python.



\## Ejecución



Desde la carpeta principal del proyecto, ejecutar:



```bash

py -m unittest test\_vetgestion -v

```



\## Pruebas realizadas



Se implementaron ocho pruebas unitarias:



1\. `test\_crear\_propietario`: comprueba la creación de un propietario.

2\. `test\_crear\_mascota`: verifica la creación de una mascota.

3\. `test\_crear\_veterinario`: comprueba la creación de un veterinario.

4\. `test\_crear\_cita`: verifica la creación de una cita.

5\. `test\_cita\_en\_espera`: comprueba el estado de una cita sin veterinario asignado.

6\. `test\_asignar\_veterinario`: verifica la asignación de un veterinario.

7\. `test\_estado\_veterinario`: comprueba el estado del veterinario.

8\. `test\_fecha\_hora\_cita`: verifica el registro de fecha y hora de la cita.



\## Resultado



En la ejecución realizada durante el desarrollo se obtuvieron ocho pruebas satisfactorias (`OK`).



Estas pruebas verifican componentes específicos del sistema y no representan una validación exhaustiva de todos los flujos de la aplicación.

