"""Private numerical primitives used by the CASTp weighted mesh."""

import numpy as np

_SIMPLEX_FACE_LOCAL_INDICES = (
    (1, 2, 3),  # face opposite vertex 0 → matches neighbors[s, 0]
    (0, 2, 3),  # face opposite vertex 1 → matches neighbors[s, 1]
    (0, 1, 3),  # face opposite vertex 2 → matches neighbors[s, 2]
    (0, 1, 2),  # face opposite vertex 3 → matches neighbors[s, 3]
)


def _tetrahedron_volumes(points_of_alpha_sphere, points):
    volumes = np.empty(len(points_of_alpha_sphere), dtype=float)
    for index, tetrahedron_indices in enumerate(points_of_alpha_sphere):
        tetrahedron_points = points[tetrahedron_indices]
        tetrahedron_matrix = np.concatenate(
            (tetrahedron_points, np.ones((4, 1))), axis=1
        )
        volumes[index] = abs(np.linalg.det(tetrahedron_matrix) / 6.0)
    return volumes


def _tetrahedron_edge_extrema(points_of_alpha_sphere, points):
    min_edges = np.empty(len(points_of_alpha_sphere), dtype=float)
    max_edges = np.empty(len(points_of_alpha_sphere), dtype=float)

    edge_pairs = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))

    for index, tetrahedron_indices in enumerate(points_of_alpha_sphere):
        tetrahedron_points = points[tetrahedron_indices]
        edge_lengths = [
            np.linalg.norm(tetrahedron_points[ii] - tetrahedron_points[jj])
            for ii, jj in edge_pairs
        ]
        min_edges[index] = min(edge_lengths)
        max_edges[index] = max(edge_lengths)

    return min_edges, max_edges


def _tetrahedron_condition_numbers(points_of_alpha_sphere, points):
    condition_numbers = np.empty(len(points_of_alpha_sphere), dtype=float)

    for index, tetrahedron_indices in enumerate(points_of_alpha_sphere):
        tetrahedron_points = points[tetrahedron_indices]
        point_a, point_b, point_c, point_d = tetrahedron_points
        matrix = 2.0 * np.vstack(
            (point_b - point_a, point_c - point_a, point_d - point_a)
        )
        condition_numbers[index] = np.linalg.cond(matrix)

    return condition_numbers


def triangle_area(points: np.ndarray) -> float:
    """Return the area of a triangle from its 3D coordinates."""

    pts = np.asarray(points, dtype=float)
    if pts.shape != (3, 3):
        return 0.0
    return float(0.5 * np.linalg.norm(np.cross(pts[1] - pts[0], pts[2] - pts[0])))
