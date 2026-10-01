# animacion_roseta.py
# Extensión voluntaria del Ejercicio 2: 20 rosetas con N de 5 a 24 juntadas en un GIF.
# Gianlucca Torreani - Taller de Programación de 5.ª Generación I
#
# Reutilizo las funciones de ejercicio2_roseta.py tal cual (por eso allá
# el programa principal está adentro del if __name__ == "__main__").

from PIL import Image
from ejercicio2_roseta import generar_puntos_circulo, dibujar_roseta

ancho, alto = 700, 700
cuadros = []

for n in range(5, 25):  # 5, 6, ..., 24 -> 20 cuadros
    img = Image.new("RGB", (ancho, alto), "black")
    pixels = img.load()
    puntos = generar_puntos_circulo(350, 350, 300, n)
    dibujar_roseta(pixels, puntos, ancho, alto)
    cuadros.append(img)
    print(f"cuadro N={n} listo")

# cada cuadro dura 250 ms, el último lo dejo más tiempo para que se aprecie
duraciones = [250] * (len(cuadros) - 1) + [1500]
cuadros[0].save("roseta_animada.gif", save_all=True, append_images=cuadros[1:],
                duration=duraciones, loop=0)
print("Listo: roseta_animada.gif con", len(cuadros), "cuadros")
