import math
import random

def generate_convex_polygon(n: int, radius: float = 100.0):
    angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n)])
    points = [(radius * math.cos(a), radius * math.sin(a)) for a in angles]
    # Redondear al entero más cercano y convertir a float con .0 (ej. 12.0)
    return [(float(round(x)), float(round(y))) for x, y in points]

def generate_test_file(filename: str = "pruebas_convex_hull.txt", count: int = 30, step: int = 10, start: int = 10):
    with open(filename, "w") as f:
        for i in range(count):
            n_points = start + i * step
            points = generate_convex_polygon(n_points)
            # Construir línea como: Prueba1|x1,y1|x2,y2|...
            line = f"Prueba{i+1}"
            for x, y in points:
                line += f"|{x:.1f},{y:.1f}"
            f.write(line + "\n")
    print(f"Archivo '{filename}' generado con {count} pruebas.")

if __name__ == "__main__":
    generate_test_file()