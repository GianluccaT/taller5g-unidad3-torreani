# taller5g-unidad3-torreani

Tarea práctica de la **Unidad III — Conversión por rastreo** (algoritmos DDA y Bresenham).

- **Materia:** Taller de Programación de 5.ª Generación I — Universidad Americana
- **Docente:** Prof. Mgtr. Alberto F. Giménez Méndez
- **Alumno:** Gianlucca Torreani

## Qué hay acá

| Archivo | Qué hace |
|---|---|
| `ejercicio1_casa.py` | Casa con techo, puerta, 2 ventanas, sol de 24 rayos y piso, todo con `dda()`. Extras: árboles, nubes, chimenea con humo y degradés. Genera `casa.png`. |
| `ejercicio2_roseta.py` | Rosetas con `bresenham()` uniendo N puntos de una circunferencia, con degradé por ángulo y distancia al centro. Genera `roseta.png`, `roseta_12.png`, `roseta_24.png`, `roseta_36.png` y los extras `roseta_salto5.png` y `roseta_complementaria.png`. |
| `animacion_roseta.py` | Extra: 20 rosetas con N de 5 a 24 en `roseta_animada.gif`. |

Las funciones `dda()` y `bresenham()` son las de clase, sin tocar la firma.

## Cómo correrlo

Se necesita Python 3 y Pillow:

```bash
pip install -r requirements.txt
python ejercicio1_casa.py
python ejercicio2_roseta.py
python animacion_roseta.py   # opcional, el GIF
```

Las imágenes se generan en la misma carpeta desde donde se ejecuta.
