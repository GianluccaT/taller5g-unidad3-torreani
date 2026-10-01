# ejercicio1_casa.py
# Tarea Unidad III - Ejercicio 1: casita armada solo con DDA
# Gianlucca Torreani - Taller de Programación de 5.ª Generación I
#
# La idea es simple: todo lo que se ve en la imagen sale de llamar a dda().
# Hasta los "rellenos" (cielo, pasto, paredes) son líneas horizontales una
# debajo de la otra, no hay ningún draw ni fill de Pillow metido de contrabando.

from PIL import Image
import math


def dda(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una linea usando el algoritmo DDA."""
    dx, dy = x1 - x0, y1 - y0
    pasos = max(abs(dx), abs(dy))
    if pasos == 0:
        return
    x_inc, y_inc = dx / pasos, dy / pasos
    x, y = x0, y0
    for _ in range(int(pasos) + 1):
        px, py = round(x), round(y)
        if 0 <= px < ancho and 0 <= py < alto:
            pixels[px, py] = color
        x += x_inc
        y += y_inc


# ------------------------------------------------------------------
# Helpers de color
# ------------------------------------------------------------------

def mezclar(c1, c2, t):
    """Mezcla dos colores RGB. t=0 devuelve c1, t=1 devuelve c2.
    La uso para todos los degradés, así no repito la cuenta en cada lado."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


# ------------------------------------------------------------------
# Figuras básicas (las que pide la consigna)
# ------------------------------------------------------------------

def dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Rectángulo con las 4 líneas de siempre: arriba, derecha, abajo, izquierda."""
    dda(pixels, x0, y0, x1, y0, color, ancho, alto)  # lado de arriba
    dda(pixels, x1, y0, x1, y1, color, ancho, alto)  # lado derecho
    dda(pixels, x1, y1, x0, y1, color, ancho, alto)  # lado de abajo
    dda(pixels, x0, y1, x0, y0, color, ancho, alto)  # lado izquierdo


def rellenar_rectangulo(pixels, x0, y0, x1, y1, color_arriba, color_abajo, ancho, alto):
    """Pinta el interior de un rectángulo con líneas horizontales.
    Si le paso dos colores distintos me queda un degradé vertical, de yapa."""
    filas = max(1, y1 - y0)
    for y in range(y0, y1 + 1):
        t = (y - y0) / filas
        dda(pixels, x0, y, x1, y, mezclar(color_arriba, color_abajo, t), ancho, alto)


def dibujar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    """Tres llamadas a dda() uniendo los vértices, nada más."""
    dda(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)
    dda(pixels, p2[0], p2[1], p3[0], p3[1], color, ancho, alto)
    dda(pixels, p3[0], p3[1], p1[0], p1[1], color, ancho, alto)


def rellenar_triangulo(pixels, punta, base_izq, base_der, color_arriba, color_abajo, ancho, alto):
    """Relleno para triángulos con la base horizontal (techo y copas de árbol).
    Bajo fila por fila desde la punta y en cada fila calculo dónde cortan
    los dos lados inclinados, después tiro una línea entre esos dos x."""
    y_top, y_base = punta[1], base_izq[1]
    altura = max(1, y_base - y_top)
    for y in range(y_top, y_base + 1):
        t = (y - y_top) / altura  # 0 en la punta, 1 en la base
        x_izq = punta[0] + (base_izq[0] - punta[0]) * t
        x_der = punta[0] + (base_der[0] - punta[0]) * t
        dda(pixels, round(x_izq), y, round(x_der), y,
            mezclar(color_arriba, color_abajo, t), ancho, alto)


# ------------------------------------------------------------------
# Elementos de la casa
# ------------------------------------------------------------------

def dibujar_cuerpo_casa(pixels, x0, y0, x1, y1, ancho, alto):
    """Paredes: primero las pinto color crema y después el contorno marrón."""
    rellenar_rectangulo(pixels, x0, y0, x1, y1, (255, 240, 205), (240, 215, 170), ancho, alto)
    dibujar_rectangulo(pixels, x0, y0, x1, y1, (110, 70, 40), ancho, alto)


def dibujar_techo(pixels, punta, base_izq, base_der, ancho, alto):
    """Techo de tejas: degradé de rojo oscuro arriba a naranja abajo."""
    rellenar_triangulo(pixels, punta, base_izq, base_der, (150, 30, 30), (230, 100, 50), ancho, alto)
    dibujar_triangulo(pixels, punta, base_izq, base_der, (90, 15, 15), ancho, alto)


def dibujar_puerta(pixels, x0, y0, x1, y1, ancho, alto):
    """Puerta de madera con su picaporte."""
    rellenar_rectangulo(pixels, x0, y0, x1, y1, (150, 90, 45), (110, 60, 30), ancho, alto)
    dibujar_rectangulo(pixels, x0, y0, x1, y1, (60, 30, 10), ancho, alto)

    # el picaporte es una crucecita dorada, cerca del borde derecho
    px, py = x1 - 10, (y0 + y1) // 2
    dorado = (240, 200, 40)
    dda(pixels, px - 3, py, px + 3, py, dorado, ancho, alto)
    dda(pixels, px, py - 3, px, py + 3, dorado, ancho, alto)


def dibujar_ventana(pixels, x, y, lado, ancho, alto):
    """Ventana cuadrada: vidrio celeste, marco blanco y la cruz del medio.
    Recibe la esquina de arriba a la izquierda y el tamaño del lado."""
    x1, y1 = x + lado, y + lado
    rellenar_rectangulo(pixels, x, y, x1, y1, (170, 220, 255), (90, 160, 220), ancho, alto)
    blanco = (255, 255, 255)
    dibujar_rectangulo(pixels, x, y, x1, y1, blanco, ancho, alto)
    # marco doble para que se note más
    dibujar_rectangulo(pixels, x - 1, y - 1, x1 + 1, y1 + 1, (70, 70, 70), ancho, alto)
    # la cruz que divide los cuatro vidrios
    dda(pixels, x + lado // 2, y, x + lado // 2, y1, blanco, ancho, alto)
    dda(pixels, x, y + lado // 2, x1, y + lado // 2, blanco, ancho, alto)


def dibujar_sol(pixels, cx, cy, radio, n_rayos, color, ancho, alto):
    """Sol con rayos que salen todos del mismo centro (cálculo polar).
    Alterno rayos largos y cortos y les voy cambiando el color de
    amarillo a naranja. El 'disco' del medio también son rayos, pero
    muchísimos y cortitos, así que queda relleno sin usar otra cosa que dda()."""
    # núcleo: 360 rayos de un tercio del radio, uno por grado
    for g in range(360):
        a = math.radians(g)
        dda(pixels, cx, cy, cx + int(radio * 0.38 * math.cos(a)), cy + int(radio * 0.38 * math.sin(a)),
            color, ancho, alto)

    # rayos de verdad
    for i in range(n_rayos):
        angulo = 2 * math.pi * i / n_rayos
        largo = radio if i % 2 == 0 else radio * 0.7  # uno largo, uno corto
        x = cx + int(largo * math.cos(angulo))
        y = cy + int(largo * math.sin(angulo))
        t = i / n_rayos
        color_rayo = mezclar(color, (255, 140, 0), abs(math.sin(t * math.pi)))
        dda(pixels, cx, cy, x, y, color_rayo, ancho, alto)


def dibujar_piso(pixels, y, color, ancho, alto):
    """Línea de piso de punta a punta de la imagen."""
    dda(pixels, 0, y, ancho - 1, y, color, ancho, alto)


# ------------------------------------------------------------------
# Extensiones voluntarias (árboles, nubes, chimenea y humo)
# ------------------------------------------------------------------

def dibujar_arbol(pixels, x_base, y_piso, ancho, alto):
    """Árbol: tronco rectangular + copa triangular, como pide la extensión.
    Le pongo dos triángulos en la copa porque con uno solo parecía cono de tránsito."""
    # tronco
    rellenar_rectangulo(pixels, x_base - 8, y_piso - 45, x_base + 8, y_piso,
                        (120, 75, 40), (90, 55, 25), ancho, alto)
    dibujar_rectangulo(pixels, x_base - 8, y_piso - 45, x_base + 8, y_piso, (60, 35, 15), ancho, alto)

    # copa en dos pisos, la de arriba más clarita
    verde_oscuro = (20, 90, 30)
    abajo = ((x_base, y_piso - 130), (x_base - 45, y_piso - 45), (x_base + 45, y_piso - 45))
    arriba = ((x_base, y_piso - 170), (x_base - 35, y_piso - 100), (x_base + 35, y_piso - 100))
    rellenar_triangulo(pixels, *abajo, (60, 160, 60), (30, 110, 40), ancho, alto)
    dibujar_triangulo(pixels, *abajo, verde_oscuro, ancho, alto)
    rellenar_triangulo(pixels, *arriba, (110, 200, 90), (50, 140, 50), ancho, alto)
    dibujar_triangulo(pixels, *arriba, verde_oscuro, ancho, alto)


def dibujar_bolita(pixels, cx, cy, rx, ry, color_arriba, color_abajo, ancho, alto):
    """Elipse rellena hecha con líneas horizontales cortas.
    Para cada fila calculo cuánto mide el ancho de la elipse en esa altura
    (la fórmula de la elipse despejada) y tiro una línea de ese largo.
    La uso para las nubes y para las bocanadas de humo."""
    for k in range(-int(ry), int(ry) + 1):
        mitad = rx * math.sqrt(max(0, 1 - (k / ry) ** 2))
        t = (k + ry) / (2 * ry)  # 0 arriba, 1 abajo
        dda(pixels, int(cx - mitad), int(cy + k), int(cx + mitad), int(cy + k),
            mezclar(color_arriba, color_abajo, t), ancho, alto)


def dibujar_nube(pixels, cx, cy, escala, ancho, alto):
    """Nube = tres bolitas pegadas. Abajo queda un poco más gris, tipo sombrita."""
    bolitas = [(-25, 5, 22, 14), (0, -6, 28, 20), (27, 4, 22, 14)]  # (dx, dy, radio_x, radio_y)
    for dx, dy, rx, ry in bolitas:
        dibujar_bolita(pixels, cx + dx * escala, cy + dy * escala, rx * escala, ry * escala,
                       (255, 255, 255), (215, 225, 235), ancho, alto)


def dibujar_chimenea(pixels, x0, x1, y_top, y_izq, y_der, ancho, alto):
    """Chimenea apoyada en el techo. Como el techo está inclinado, el lado
    derecho baja más que el izquierdo (por eso le paso dos alturas)."""
    ladrillo = (140, 60, 45)
    for x in range(x0, x1 + 1):
        # relleno con líneas verticales hasta donde toca el techo
        y_fin = round(y_izq + (y_der - y_izq) * (x - x0) / (x1 - x0))
        dda(pixels, x, y_top, x, y_fin, ladrillo, ancho, alto)
    borde = (70, 25, 15)
    dda(pixels, x0 - 3, y_top, x1 + 3, y_top, borde, ancho, alto)  # el "sombrerito" de arriba
    dda(pixels, x0, y_top, x0, y_izq, borde, ancho, alto)
    dda(pixels, x1, y_top, x1, y_der, borde, ancho, alto)


def dibujar_humo(pixels, x, y, ancho, alto):
    """Humo: bocanadas que suben, se corren un poco a la derecha (viento),
    se agrandan y se van aclarando hasta casi mezclarse con el cielo."""
    bocanadas = 6
    for i in range(bocanadas):
        t = i / (bocanadas - 1)
        bx = x + i * 9 + (4 if i % 2 else -4)  # un vaivén chiquito para que no suba recto
        by = y - 8 - i * 17
        r = 6 + i * 2.5
        gris = mezclar((120, 120, 125), (230, 235, 240), t)
        dibujar_bolita(pixels, bx, by, r, r * 0.8, gris, mezclar(gris, (90, 90, 95), 0.3), ancho, alto)


# ------------------------------------------------------------------
# Programa principal
# ------------------------------------------------------------------

ancho, alto = 600, 500
imagen = Image.new("RGB", (ancho, alto), (200, 230, 255))
pixels = imagen.load()

Y_PISO = 400  # todo se apoya acá

# 1) Fondo: cielo con degradé (azul arriba, celeste clarito abajo) y pasto
rellenar_rectangulo(pixels, 0, 0, ancho - 1, Y_PISO, (90, 160, 230), (205, 235, 255), ancho, alto)
rellenar_rectangulo(pixels, 0, Y_PISO, ancho - 1, alto - 1, (90, 180, 70), (40, 110, 35), ancho, alto)

# 2) Sol arriba a la izquierda, 24 rayos (la consigna pide mínimo 8, me fui un poco)
dibujar_sol(pixels, 80, 80, 62, 24, (255, 230, 60), ancho, alto)

# 3) Nubes
dibujar_nube(pixels, 230, 60, 1.0, ancho, alto)
dibujar_nube(pixels, 480, 95, 0.8, ancho, alto)

# 4) Árboles a los costados de la casa
dibujar_arbol(pixels, 75, Y_PISO, ancho, alto)
dibujar_arbol(pixels, 525, Y_PISO, ancho, alto)

# 5) La casa en sí. Los puntos del techo los dejo en variables
#    porque la chimenea los necesita para calcular dónde se apoya.
punta, techo_izq, techo_der = (300, 120), (160, 230), (440, 230)

def y_en_techo(x):
    """Devuelve la altura del lado derecho del techo en una x dada (recta entre punta y techo_der)."""
    return round(punta[1] + (techo_der[1] - punta[1]) * (x - punta[0]) / (techo_der[0] - punta[0]))

dibujar_chimenea(pixels, 360, 385, 140, y_en_techo(360), y_en_techo(385), ancho, alto)
dibujar_humo(pixels, 372, 136, ancho, alto)  # sale justo por arriba de la chimenea
dibujar_techo(pixels, punta, techo_izq, techo_der, ancho, alto)
dibujar_cuerpo_casa(pixels, 180, 230, 420, Y_PISO, ancho, alto)
dibujar_puerta(pixels, 275, 320, 325, Y_PISO, ancho, alto)
dibujar_ventana(pixels, 205, 260, 50, ancho, alto)
dibujar_ventana(pixels, 345, 260, 50, ancho, alto)

# 6) Por último la línea de piso, encima de todo para que se vea bien
dibujar_piso(pixels, Y_PISO, (50, 50, 50), ancho, alto)

imagen.save("casa.png")
print("Listo, se generó casa.png")
