# CTE334-Actividad03: Planificador de vuelo fotogramétrico con dron

**Estudiante:** Daniel Sierra
**Número de cuenta:** 20201004160

## Descripción y objetivo

Esta aplicación sirve para planificar, de forma básica, un vuelo con dron para tomar fotos de un terreno.

Tú escribes los datos de la cámara, del sensor, del vuelo y de la parcela. El programa hace los cálculos y te muestra:

- El tamaño de cada píxel en el sensor (RSI).
- Cuántos centímetros del terreno representa cada píxel (GSD).
- La escala del vuelo.
- El tamaño de cada foto sobre el terreno.
- La distancia entre fotos y entre pasadas.
- Cuántas pasadas y cuántas fotos se necesitan.
- La distancia total del vuelo y el tiempo estimado.

## Versión de Python y sistema operativo

- **Python:** 3.12
- **Sistema operativo para construir el `.exe`:** Windows

## Cómo ejecutar el programa

Abre una terminal en la carpeta del proyecto y escribe:

```
python Actividad_03.py
```

## Cómo reconstruir el `.exe`

Esto debe hacerse en Windows. Primero crea un entorno de Conda:

```
conda create --name actividad03 python=3.12 pyinstaller -y
conda activate actividad03
```

Luego genera el ejecutable:

```
python -m PyInstaller --onefile --windowed --name PlanificadorVueloFotogrametrico Actividad_03.py
```

El archivo final queda en la carpeta `dist/`.

## Caso de prueba

Usa estos valores (vienen en el botón **Cargar ejemplo**):

| Dato | Valor |
|---|---|
| Distancia focal | 3.61 mm |
| Ancho de imagen | 4000 píxeles |
| Alto de imagen | 3000 píxeles |
| Ancho del sensor | 6.3175 mm |
| Alto del sensor | 4.7381 mm |
| Altura de vuelo | 120 m |
| Traslape longitudinal | 80 % |
| Traslape transversal | 70 % |
| Velocidad | 8 m/s |
| Largo de la parcela | 700 m |
| Ancho de la parcela | 250 m |

**Resultados esperados:**

| Resultado | Valor |
|---|---|
| RSI | 0.001579 mm/píxel |
| GSD | 5.25 cm/píxel |
| Escala | 1 : 33,241 |
| Ancho de imagen en terreno | 210.00 m |
| Alto de imagen en terreno | 157.50 m |
| Base aérea | 42.00 m |
| Distancia entre pasadas | 47.25 m |
| Intervalo entre fotos | 5.25 s |
| Número de pasadas | 5 |
| Fotos por pasada | 18 |
| Fotos totales | 94 |
| Distancia total de vuelo | 3,953.72 m |
| Duración estimada | 8.18 min |

**Pruebas de error:**

- Campo vacío: aparece una ventana que indica qué campo llenar.
- Texto en lugar de número (por ejemplo `abc`): aparece una ventana de dato no numérico.
- Velocidad igual a 0: aparece una ventana de valor no válido.
- Traslape de 100 %: aparece una ventana de traslape fuera de rango.

En todos estos casos no se muestra ningún resultado.

## Limitaciones

- Es una planificación básica. No toma en cuenta el terreno inclinado ni el viento.
- Los resultados son teóricos y sirven para fines académicos. No deben usarse para planificar un vuelo real sin revisar otras fuentes y normas.
- El `.exe` no tiene firma digital, así que Windows o el antivirus pueden mostrar una advertencia. El código fuente está en `Actividad_03.py`.

## Advertencia de uso académico

Esta aplicación fue hecha como parte de la Actividad 03 del curso CTE-334 – Desarrollo de Aplicaciones SIG, de la Universidad Nacional Autónoma de Honduras. Su uso es educativo.
