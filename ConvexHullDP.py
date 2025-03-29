from typing import List, Tuple
import matplotlib.pyplot as plt
import copy

Point = Tuple[int, int]

def cross(o: Point, a: Point, b: Point) -> int:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull_dp(points: List[Point]) -> List[Point]:
    points = sorted(points)  # Sort by x, then y
    n = len(points)

    # Tabla DP para lower hull
    dp_lower = [[] for _ in range(n)]
    for i in range(n):
        if i == 0:
            dp_lower[i] = [points[i]]
        else:
            dp_lower[i] = copy.deepcopy(dp_lower[i - 1])
            dp_lower[i].append(points[i])
            while len(dp_lower[i]) >= 3 and cross(dp_lower[i][-3], dp_lower[i][-2], dp_lower[i][-1]) <= 0:
                del dp_lower[i][-2]

    # Tabla DP para upper hull
    points_rev = list(reversed(points))
    dp_upper = [[] for _ in range(n)]
    for i in range(n):
        if i == 0:
            dp_upper[i] = [points_rev[i]]
        else:
            dp_upper[i] = copy.deepcopy(dp_upper[i - 1])
            dp_upper[i].append(points_rev[i])
            while len(dp_upper[i]) >= 3 and cross(dp_upper[i][-3], dp_upper[i][-2], dp_upper[i][-1]) <= 0:
                del dp_upper[i][-2]

    lower = dp_lower[-1]
    upper = dp_upper[-1]

    return lower[:-1] + upper[:-1]  # Eliminar duplicados en los extremos

# === Visualización ===

def plot_convex_hull(points: List[Point], hull: List[Point], title: str = "Convex Hull (DP O(n^2))") -> None:
    x_points, y_points = zip(*points)
    plt.figure(figsize=(8, 6))
    
    plt.scatter(x_points, y_points, color='blue', label='Points')
    
    if hull:
        hull_points = hull + [hull[0]]  # cerrar el polígono
        hx, hy = zip(*hull_points)
        plt.plot(hx, hy, color='green', linewidth=2, label='Convex Hull (DP)')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    pts = [(0, 0), (1, 1), (2, 2), (2, 0), (2, 4), (3, 3), (0, 3)]

    hull = convex_hull_dp(pts)
    print("Convex Hull (DP O(n^2)):", hull)

    plot_convex_hull(pts, hull, title="Convex Hull (Programación Dinámica real O(n²))")
