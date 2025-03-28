from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import math
import random

Point = Tuple[int, int]

def generate_convex_polygon(n: int, radius: float = 10.0) -> List[Point]:
    angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n)])
    points = [(radius * math.cos(a), radius * math.sin(a)) for a in angles]
    return [(round(x, 1), round(y, 1)) for x, y in points]

def area(p1: Point, p2: Point, p3: Point) -> float:
    return abs((p1[0]*(p2[1]-p3[1]) +
                p2[0]*(p3[1]-p1[1]) +
                p3[0]*(p1[1]-p2[1])) / 2.0)

def convex_hull_dp(points: List[Point]) -> Tuple[float, Dict[Tuple[int,int], int]]:
    # Assumes points are the vertices of a convex polygon in order.
    # For safety, we sort by x then y—but be sure this ordering gives a convex polygon.
    points.sort()
    n = len(points)
    memo = {}
    splits = {}
    
    def dp(i: int, j: int) -> float:
        if (i, j) in memo:
            return memo[(i, j)]
        max_area = 0
        best = None
        for k in range(i + 1, j):
            cur_area = dp(i, k) + dp(k, j) + area(points[i], points[k], points[j])
            if cur_area > max_area:
                max_area = cur_area
                best = k
        if best is not None:
            splits[(i, j)] = best
        memo[(i, j)] = max_area
        return max_area

    total_area = dp(0, n - 1)
    return total_area, splits

def extract_triangulation(splits: Dict[Tuple[int,int], int], i: int, j: int) -> List[Tuple[int,int,int]]:
    # Recursively extract the triangle indices used in the optimal triangulation.
    triangles = []
    if (i, j) in splits:
        k = splits[(i, j)]
        triangles.append((i, k, j))
        triangles.extend(extract_triangulation(splits, i, k))
        triangles.extend(extract_triangulation(splits, k, j))
    return triangles

if __name__ == "__main__":
    # Example points (should be vertices of a convex polygon in proper order)
    pts = generate_convex_polygon(12, radius=10)
    
    # Compute DP triangulation (maximum area partition)
    max_area, splits = convex_hull_dp(pts)
    triangles = extract_triangulation(splits, 0, len(pts) - 1)
    print("Máxima área poligonal (DP sobre puntos convexos):", max_area)
    
    # Prepare data for plotting.
    # For a polygon, we assume the points (after sort) are in polygon order.
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    
    # To close the polygon, add the first point at the end.
    xs.append(pts[0][0])
    ys.append(pts[0][1])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
    
    # "Before" plot: just the polygon boundary and points.
    ax1.plot(xs, ys, 'k-', lw=2)
    ax1.scatter(xs, ys, color='red', zorder=5)
    ax1.set_title("Antes: Polígono original")
    ax1.set_aspect('equal', adjustable='box')
    
    # "After" plot: polygon with triangulation lines added.
    ax2.plot(xs, ys, 'k-', lw=2, label="Borde del polígono")
    ax2.scatter(xs, ys, color='red', zorder=5)
    
    # Draw the triangulation edges.
    # For every triangle, plot its boundary (in a different color/dashed).
    for tri in triangles:
        i, k, j = tri
        tri_x = [pts[i][0], pts[k][0], pts[j][0], pts[i][0]]
        tri_y = [pts[i][1], pts[k][1], pts[j][1], pts[i][1]]
        ax2.plot(tri_x, tri_y, 'b--', lw=1)
    
    ax2.set_title("Después: Triangulación óptima")
    ax2.set_aspect('equal', adjustable='box')
    plt.show()