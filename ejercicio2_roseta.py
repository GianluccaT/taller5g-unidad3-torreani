# ejercicio2_roseta.py
# Tarea Unidad III - Ejercicio 2: rosetas tipo mandala con Bresenham
# Gianlucca Torreani - Taller de Programación de 5.ª Generación I
#
# Reparto N puntos en una circunferencia (que NO se dibuja) y uno cada
# punto con todos los demás. Con N=24 son 24*23/2 = 276 líneas.
# El color de cada línea sale del ángulo de su punto medio (tono) y de
# qué tan cerca pasa del centro (brillo), así el degradé va por los dos lados.

from PIL import Image
import math
import colorsys


def bresenham(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Bresenham generalizado, aritmetica entera exclusivamente."""
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        if 0 <= x < ancho and 0 <= y < alto:
            pixels[x, y] = color
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def generar_puntos_circulo(cx, cy, radio, n):
    """Devuelve n puntos equiespaciados sobre la circunferencia.
    Uso int() porque bresenham trabaja solo con enteros."""
    puntos = []
    for i in range(n):
        angulo = 2 * math.pi * i / n
        x = cx + int(radio * math.cos(angulo))
        y = cy + int(radio * math.sin(angulo))
        puntos.append((x, y))
    return puntos


def color_gradiente(x0, y0, x1, y1, cx, cy, radio, tono_base=0.0, rango_tono=1.0):
    """Calcula el color de una línea según dónde está respecto al centro.

    - Tono: depende del ángulo del punto medio de la línea, entonces
      el color va girando alrededor de la roseta como un arcoíris.
    - Brillo: las líneas que pasan cerca del centro salen más claritas
      y las que quedan pegadas al borde más intensas.

    tono_base y rango_tono los uso para la variante de colores
    complementarios (ahí no quiero el arcoíris entero)."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    angulo = math.atan2(my - cy, mx - cx)              # entre -pi y pi
    t_ang = (angulo + math.pi) / (2 * math.pi)         # lo paso a 0..1
    dist = min(1.0, math.hypot(mx - cx, my - cy) / radio)  # 0 en el centro, 1 en el borde

    tono = (tono_base + t_ang * rango_tono) % 1.0
    saturacion = 0.45 + 0.55 * dist
    brillo = 1.0 - 0.25 * dist
    r, g, b = colorsys.hsv_to_rgb(tono, saturacion, brillo)
    return int(r * 255), int(g * 255), int(b * 255)


def dibujar_roseta(pixels, puntos, ancho, alto):
    """Une cada par de puntos (i, j) con j > i, así ninguna línea se repite.
    El centro y el radio los saco de los mismos puntos para no tener que
    pasarlos por parámetro (la firma queda como pide la consigna)."""
    n = len(puntos)
    cx = sum(p[0] for p in puntos) / n
    cy = sum(p[1] for p in puntos) / n
    radio = max(math.hypot(p[0] - cx, p[1] - cy) for p in puntos)

    for i in range(n):
        for j in range(i + 1, n):  # conectar cada par una sola vez
            x0, y0 = puntos[i]
            x1, y1 = puntos[j]
            color = color_gradiente(x0, y0, x1, y1, cx, cy, radio)
            bresenham(pixels, x0, y0, x1, y1, color, ancho, alto)
    return n * (n - 1) // 2  # cantidad de líneas, para mostrar en consola


# ------------------------------------------------------------------
# Extensiones voluntarias
# ------------------------------------------------------------------

def dibujar_roseta_salto(pixels, puntos, salto, ancho, alto, tono_base=0.0, rango_tono=1.0):
    """Variante: cada punto se une SOLO con el que está 'salto' lugares
    más adelante (nada de vecinos). Con N=36 y salto=5 sale una estrella
    de 36 puntas de un solo trazo, porque 36 y 5 no tienen divisores en común."""
    n = len(puntos)
    cx = sum(p[0] for p in puntos) / n
    cy = sum(p[1] for p in puntos) / n
    radio = max(math.hypot(p[0] - cx, p[1] - cy) for p in puntos)
    for i in range(n):
        x0, y0 = puntos[i]
        x1, y1 = puntos[(i + salto) % n]
        color = color_gradiente(x0, y0, x1, y1, cx, cy, radio, tono_base, rango_tono)
        bresenham(pixels, x0, y0, x1, y1, color, ancho, alto)


def roseta_complementaria(n, ancho=700, alto=700):
    """Fondo azul marino y líneas en naranjas/dorados (el complementario del azul).
    Pongo varias estrellas con saltos distintos y radios distintos, una adentro
    de la otra, para que quede tipo mandala por capas."""
    fondo = (15, 20, 60)
    img = Image.new("RGB", (ancho, alto), fondo)
    px = img.load()
    cx, cy = ancho // 2, alto // 2
    capas = [(320, 19), (240, 17), (160, 13), (90, 11)]  # (radio, salto)
    for k, (radio, salto) in enumerate(capas):
        pts = generar_puntos_circulo(cx, cy, radio, n)
        # tonos entre 0.05 y 0.15 = naranja a dorado, cada capa corrida un poquito
        dibujar_roseta_salto(px, pts, salto, ancho, alto, tono_base=0.03 + k * 0.03, rango_tono=0.10)
    return img


def generar_todo():
    ancho, alto = 700, 700

    # --- Las tres variantes obligatorias (fondo negro, se luce más el degradé) ---
    for n in [12, 24, 36]:
        img = Image.new("RGB", (ancho, alto), "black")
        pixels = img.load()
        puntos = generar_puntos_circulo(350, 350, 300, n)
        lineas = dibujar_roseta(pixels, puntos, ancho, alto)
        img.save(f"roseta_{n}.png")
        print(f"roseta_{n}.png -> {lineas} líneas")

        # la consigna también nombra roseta.png como salida, así que guardo la de N=24 con ese nombre
        if n == 24:
            img.save("roseta.png")
            print("roseta.png -> copia de la de N=24")

    # --- Extra 1: solo puntos no adyacentes, saltando de a 5 ---
    img = Image.new("RGB", (ancho, alto), "black")
    px = img.load()
    dibujar_roseta_salto(px, generar_puntos_circulo(350, 350, 300, 36), 5, ancho, alto)
    # le sumo una segunda estrella con salto 13 (en otros tonos) para que no quede tan vacía
    dibujar_roseta_salto(px, generar_puntos_circulo(350, 350, 300, 36), 13, ancho, alto, tono_base=0.5)
    img.save("roseta_salto5.png")
    print("roseta_salto5.png -> extensión: solo no adyacentes")

    # --- Extra 2: fondo de color + líneas complementarias ---
    roseta_complementaria(48).save("roseta_complementaria.png")
    print("roseta_complementaria.png -> extensión: colores complementarios")


# Lo meto en el if para poder importar las funciones desde animacion_roseta.py
# sin que se generen todas las imágenes de nuevo
if __name__ == "__main__":
    generar_todo()
