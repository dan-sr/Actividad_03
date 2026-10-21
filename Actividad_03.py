# -*- coding: utf-8 -*-
"""CTE-334 - Actividad 03: Planificación de un vuelo fotogramétrico con dron.

El archivo tiene dos partes:
  1. Lógica de cálculo (funciones que solo hacen cuentas, sin ventanas).
  2. Interfaz gráfica (ventana con Tkinter).
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox


# ---------------------------------------------------------------------------
# Datos que pide la aplicación
# (clave, etiqueta, unidad, ejemplo, grupo)
# ---------------------------------------------------------------------------

CAMPOS = [
    ("focal", "Distancia focal", "mm", "3.61", "Cámara y sensor"),
    ("ancho_imagen_px", "Ancho de imagen", "píxeles", "4000", "Cámara y sensor"),
    ("alto_imagen_px", "Alto de imagen", "píxeles", "3000", "Cámara y sensor"),
    ("ancho_sensor_mm", "Ancho del sensor", "mm", "6.3175", "Cámara y sensor"),
    ("alto_sensor_mm", "Alto del sensor", "mm", "4.7381", "Cámara y sensor"),
    ("altura_vuelo_m", "Altura de vuelo", "m", "120", "Parámetros de vuelo"),
    ("traslape_longitudinal", "Traslape longitudinal", "%", "80", "Parámetros de vuelo"),
    ("traslape_transversal", "Traslape transversal", "%", "70", "Parámetros de vuelo"),
    ("velocidad_m_s", "Velocidad", "m/s", "8", "Parámetros de vuelo"),
    ("largo_parcela_m", "Largo", "m", "700", "Parcela"),
    ("ancho_parcela_m", "Ancho", "m", "250", "Parcela"),
]

# Estos dos campos solo aceptan de 0 hasta menos de 100
TRASLAPES = {"traslape_longitudinal", "traslape_transversal"}


class ErrorDeDatos(Exception):
    """Un dato no sirve. Guarda el título y el mensaje para la ventana emergente."""

    def __init__(self, titulo, mensaje):
        super().__init__(mensaje)
        self.titulo = titulo
        self.mensaje = mensaje


# ---------------------------------------------------------------------------
# Lógica de cálculo (no usa widgets)
# ---------------------------------------------------------------------------

def leer_datos(textos):
    """Convierte los textos a números y revisa que sean válidos.

    textos: diccionario {clave: texto escrito en la caja}.
    Retorna un diccionario con los números.
    Si algo está mal, lanza ErrorDeDatos con un mensaje que explica qué corregir.
    """
    datos = {}
    for clave, etiqueta, unidad, ejemplo, _grupo in CAMPOS:
        texto = textos[clave].strip()

        if texto == "":
            raise ErrorDeDatos(
                "Campo vacío",
                f"Escriba un valor en «{etiqueta}» ({unidad}).",
            )

        try:
            numero = float(texto)
        except ValueError:
            numero = None

        if numero is None or not math.isfinite(numero):
            raise ErrorDeDatos(
                "Dato no numérico",
                f"«{texto}» no es un número válido en «{etiqueta}». "
                f"Escriba solo números, por ejemplo {ejemplo}.",
            )

        if clave in TRASLAPES:
            if not 0 <= numero < 100:
                raise ErrorDeDatos(
                    "Traslape fuera de rango",
                    f"«{etiqueta}» debe estar entre 0 y menos de 100 %.",
                )
        elif numero <= 0:
            raise ErrorDeDatos(
                "Valor no válido",
                f"«{etiqueta}» debe ser mayor que cero ({unidad}).",
            )

        datos[clave] = numero
    return datos


def calcular_plan_vuelo(datos):
    """Calcula todos los resultados del plan de vuelo.

    datos: diccionario con los 11 números ya validados.
    Retorna un diccionario con los resultados.
    """
    # 1. Relación sensor-imagen, resolución en el terreno y escala
    rsi = datos["ancho_sensor_mm"] / datos["ancho_imagen_px"]
    gsd_cm = datos["altura_vuelo_m"] * 100 / datos["focal"] * rsi
    escala = datos["altura_vuelo_m"] / (datos["focal"] / 1000)

    # 2. Tamaño de la foto en el terreno, distancia entre fotos y entre pasadas
    ancho_terreno = datos["ancho_sensor_mm"] * escala / 1000
    alto_terreno = datos["alto_sensor_mm"] * escala / 1000
    base = ancho_terreno * (1 - datos["traslape_longitudinal"] / 100)
    separacion = alto_terreno * (1 - datos["traslape_transversal"] / 100)
    intervalo = base / datos["velocidad_m_s"]

    # 3. Pasadas, fotos y tiempo (se usan valores sin redondear)
    pasadas_teoricas = datos["ancho_parcela_m"] / separacion
    fotos_por_pasada_teoricas = datos["largo_parcela_m"] / base + 1
    fotos_totales_teoricas = pasadas_teoricas * fotos_por_pasada_teoricas
    distancia_total = pasadas_teoricas * datos["largo_parcela_m"] + datos["ancho_parcela_m"]
    duracion_min = fotos_totales_teoricas * intervalo / 60

    return {
        "rsi": rsi,
        "gsd_cm": gsd_cm,
        "escala": escala,
        "ancho_terreno": ancho_terreno,
        "alto_terreno": alto_terreno,
        "base": base,
        "separacion": separacion,
        "intervalo": intervalo,
        "pasadas": round(pasadas_teoricas),
        "fotos_por_pasada": round(fotos_por_pasada_teoricas),
        "fotos_totales": math.ceil(fotos_totales_teoricas),
        "distancia_total": distancia_total,
        "duracion_min": duracion_min,
    }


def formatear_resultados(r):
    """Arma el texto del informe, con unidades en cada línea."""
    linea = "-" * 52
    return "\n".join([
        linea,
        "RESULTADOS DEL PLAN DE VUELO",
        linea,
        f"RSI (tamaño sensor-imagen): {r['rsi']:.6f} mm/píxel",
        f"GSD (resolución en terreno): {r['gsd_cm']:.2f} cm/píxel",
        f"Escala: 1 : {r['escala']:,.0f}",
        f"Ancho de imagen en terreno: {r['ancho_terreno']:.2f} m",
        f"Alto de imagen en terreno: {r['alto_terreno']:.2f} m",
        f"Base aérea (avance entre fotos): {r['base']:.2f} m",
        f"Distancia entre pasadas: {r['separacion']:.2f} m",
        f"Intervalo entre fotografías: {r['intervalo']:.2f} s",
        f"Número de pasadas: {r['pasadas']}",
        f"Fotografías por pasada: {r['fotos_por_pasada']}",
        f"Fotografías totales: {r['fotos_totales']}",
        f"Distancia total de vuelo: {r['distancia_total']:,.2f} m",
        f"Duración estimada: {r['duracion_min']:.2f} min",
        linea,
    ])


# ---------------------------------------------------------------------------
# Interfaz gráfica
# ---------------------------------------------------------------------------

def construir_formulario(contenedor):
    """Crea los grupos de entrada. Retorna {clave: caja de texto}."""
    cajas = {}
    marcos = {}
    filas = {}

    for clave, etiqueta, unidad, _ejemplo, grupo in CAMPOS:
        if grupo not in marcos:
            marco = ttk.LabelFrame(contenedor, text=grupo, padding=8)
            marco.grid(row=len(marcos), column=0, sticky="ew", pady=4)
            marcos[grupo] = marco
            filas[grupo] = 0

        marco = marcos[grupo]
        fila = filas[grupo]
        ttk.Label(marco, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=2)
        caja = ttk.Entry(marco, width=14)
        caja.grid(row=fila, column=1, padx=6, pady=2)
        ttk.Label(marco, text=unidad).grid(row=fila, column=2, sticky="w")
        filas[grupo] = fila + 1

        cajas[clave] = caja

    return cajas


def main():
    """Crea la ventana y la deja abierta."""
    ventana = tk.Tk()
    ventana.title("Planificador de vuelo fotogramétrico con dron")
    ventana.resizable(False, False)

    marco = ttk.Frame(ventana, padding=12)
    marco.grid(row=0, column=0, sticky="nsew")

    ttk.Label(
        marco,
        text="Planificación de vuelo fotogramétrico",
        font=("TkDefaultFont", 13, "bold"),
    ).grid(row=0, column=0, sticky="w")
    ttk.Label(marco, text="Escriba los datos en las unidades indicadas.").grid(
        row=1, column=0, sticky="w", pady=(0, 6)
    )

    formulario = ttk.Frame(marco)
    formulario.grid(row=2, column=0, sticky="ew")
    cajas = construir_formulario(formulario)

    estado = tk.StringVar(value="Listo.")

    def mostrar_texto(texto):
        salida.config(state="normal")
        salida.delete("1.0", tk.END)
        salida.insert("1.0", texto)
        salida.config(state="disabled")

    def ejecutar_calculo():
        textos = {clave: caja.get() for clave, caja in cajas.items()}
        try:
            datos = leer_datos(textos)
        except ErrorDeDatos as error:
            messagebox.showerror(error.titulo, error.mensaje)
            estado.set("Corrija el dato indicado y vuelva a calcular.")
            return  # no se muestra ningún resultado parcial

        resultados = calcular_plan_vuelo(datos)
        mostrar_texto(formatear_resultados(resultados))
        estado.set("Cálculo completado.")

    def limpiar():
        for caja in cajas.values():
            caja.delete(0, tk.END)
        mostrar_texto("")
        estado.set("Campos y resultados limpiados.")

    def cargar_ejemplo():
        for clave, _etiqueta, _unidad, ejemplo, _grupo in CAMPOS:
            cajas[clave].delete(0, tk.END)
            cajas[clave].insert(0, ejemplo)
        estado.set("Ejemplo cargado. Presione Calcular.")

    botones = ttk.Frame(marco)
    botones.grid(row=3, column=0, pady=8)
    ttk.Button(botones, text="Calcular", command=ejecutar_calculo).grid(row=0, column=0, padx=4)
    ttk.Button(botones, text="Limpiar", command=limpiar).grid(row=0, column=1, padx=4)
    ttk.Button(botones, text="Cargar ejemplo", command=cargar_ejemplo).grid(row=0, column=2, padx=4)

    ttk.Label(marco, textvariable=estado).grid(row=4, column=0, sticky="w")

    marco_resultados = ttk.LabelFrame(marco, text="Resultados", padding=6)
    marco_resultados.grid(row=5, column=0, sticky="ew", pady=(6, 0))
    salida = tk.Text(marco_resultados, width=56, height=17, font="TkFixedFont", state="disabled")
    salida.grid(row=0, column=0, sticky="nsew")

    ventana.mainloop()


if __name__ == "__main__":
    main()
