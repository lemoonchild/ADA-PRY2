from typing import List, Tuple
import matplotlib.pyplot as plt
import time

Point = Tuple[int, int]

def leer_prueba(numero: int, archivo: str = "pruebas_convex_hull.txt") -> List[Point]:
    with open(archivo, "r") as f:
        lineas = f.readlines()
        if numero < 1 or numero > len(lineas):
            raise ValueError("Número de prueba fuera de rango")
        linea = lineas[numero - 1].strip()
        partes = linea.split("|")[1:]  # ignorar "PruebaX"
        puntos = []
        for p in partes:
            x_str, y_str = p.split(",")
            puntos.append((float(x_str), float(y_str)))
        return puntos

def cross(o: Point, a: Point, b: Point) -> int:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def merge(left: List[Point], right: List[Point]) -> List[Point]:
    points = left + right
    points.sort()

    upper = []
    for p in points:
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    lower = []
    for p in reversed(points):
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    return upper[:-1] + lower[:-1]  # without duplicating first point

def divide_and_conquer(points: List[Point]) -> List[Point]:
    if len(points) <= 1:
        return points
    points.sort()
    mid = len(points) // 2
    left_hull = divide_and_conquer(points[:mid])
    right_hull = divide_and_conquer(points[mid:])
    return merge(left_hull, right_hull)

def plot_points(points: List[Point]) -> None:
    x_points, y_points = zip(*points)
    plt.figure(figsize=(8, 6))
    plt.scatter(x_points, y_points, color='blue', label='Points')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Original Points')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_convex_hull(points: List[Point], hull: List[Point]) -> None:
    # Unzip points for plotting
    x_points, y_points = zip(*points)
    plt.figure(figsize=(8, 6))
    
    # Plot original points
    plt.scatter(x_points, y_points, color='blue', label='Points')
    
    # Plot convex hull if exists
    if hull:
        hull_points = hull + [hull[0]]  # closes the polygon
        hx, hy = zip(*hull_points)
        plt.plot(hx, hy, color='red', linewidth=2, label='Convex Hull')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Convex Hull (Divide and Conquer)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    print("Benchmarking Divide and Conquer:")
    for i in range(1, 31):
        puntos = leer_prueba(i)
        start = time.perf_counter()
        hull = divide_and_conquer(puntos)
        end = time.perf_counter()
        elapsed = end - start
        print(f"Prueba {i:02d} | Puntos: {len(puntos):3d} | Tiempo: {elapsed:.6f} segundos")
    
    # pts = [(0, 0), (1, 1), (2, 2), (2, 0), (2, 4), (3, 3), (0, 3)]
    
    # # Show points before computing the hull
    # plot_points(pts)
    
    # # Compute the convex hull
    # hull = divide_and_conquer(pts)
    # print("Convex Hull (DaC):", hull)
    
    # # Show points after adding the convex hull
    # plot_convex_hull(pts, hull)
