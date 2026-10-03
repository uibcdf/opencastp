"""Independent geometric volume reference using planar disk boundaries.

This developer tool imports no CASTp metric primitive or alpha predicate.
It integrates the complement of an explicit sphere union inside a supplied
tetrahedron. Domains and spheres are caller inputs, not independently detected.
QUADPACK error estimates are not certified interval bounds; retain convergence
messages and compare refinements/orientations before interpreting a result.
"""

from itertools import combinations
from math import acos, atan2, cos, fsum, pi, sin, sqrt

import numpy as np
from scipy.integrate import quad


def _cross(first: np.ndarray, second: np.ndarray) -> float:
    return float(first[0] * second[1] - first[1] * second[0])


def _polygon_signed_area(polygon: np.ndarray) -> float:
    return 0.5 * fsum(
        _cross(p, q) for p, q in zip(polygon, np.roll(polygon, -1, axis=0), strict=True)
    )


def _segment_circle_roots(
    first: np.ndarray, delta: np.ndarray, center: np.ndarray, radius: float
) -> list[float]:
    offset = first - center
    a = float(delta @ delta)
    if a == 0:
        return []
    b = float(offset @ delta)
    discriminant = b * b - a * float(offset @ offset - radius * radius)
    if discriminant < 0:
        return []
    root = sqrt(discriminant)
    return [t for t in ((-b - root) / a, (-b + root) / a) if 0 <= t <= 1]


def uncovered_polygon_area(
    polygon: np.ndarray, centers: np.ndarray, radii: np.ndarray
) -> float:
    """Integrate the boundary of a convex polygon minus a union of disks.

    Straight uncovered polygon segments contribute counterclockwise; exposed
    disk arcs inside the polygon contribute clockwise. Their Green integrals
    give area without inclusion/exclusion of CASTp spherical primitives.
    Inputs use one caller-declared length unit. The result uses its square.
    """
    polygon, centers, radii = map(
        lambda x: np.asarray(x, dtype=float), (polygon, centers, radii)
    )
    if (
        polygon.ndim != 2
        or polygon.shape[1] != 2
        or centers.shape != (len(radii), 2)
        or radii.ndim != 1
    ):
        raise ValueError("Polygon, disk center and radius shapes differ")
    if not all(
        np.all(np.isfinite(value)) for value in (polygon, centers, radii)
    ) or np.any(radii < 0):
        raise ValueError("Geometry must be finite and radii non-negative")
    if len(polygon) < 3:
        return 0.0
    origin = polygon.mean(axis=0)
    polygon, centers = polygon - origin, centers - origin
    polygon_area = _polygon_signed_area(polygon)
    if polygon_area < 0:
        polygon = polygon[::-1]
        polygon_area = -polygon_area
    if polygon_area == 0:
        return 0.0
    scale = max(float(np.max(np.abs(polygon))), 1.0)
    tolerance = 2e-13 * scale**2
    edges = [
        (p, q - p) for p, q in zip(polygon, np.roll(polygon, -1, axis=0), strict=True)
    ]
    if any(
        _cross(delta, point - p) < -tolerance for p, delta in edges for point in polygon
    ):
        raise ValueError("Polygon must be convex")
    if not len(radii):
        return polygon_area
    nearest_box = np.maximum(
        np.maximum(polygon.min(axis=0) - centers, centers - polygon.max(axis=0)), 0.0
    )
    keep = np.sum(nearest_box**2, axis=1) <= radii**2
    disks = np.unique(np.column_stack((centers[keep], radii[keep])), axis=0)
    disks = disks[disks[:, 2] > 0]
    centers, radii = disks[:, :2], disks[:, 2]
    if not len(radii):
        return polygon_area
    radii_squared = radii**2
    if np.any(
        np.all(
            np.sum((polygon[None, :, :] - centers[:, None, :]) ** 2, axis=2)
            <= radii_squared[:, None],
            axis=1,
        )
    ):
        return 0.0
    line_terms = []
    angles = [[0.0, 2 * pi] for _radius in radii]
    for p, delta in edges:
        breaks = [0.0, 1.0]
        for index, (center, radius) in enumerate(zip(centers, radii, strict=True)):
            for t in _segment_circle_roots(p, delta, center, float(radius)):
                breaks.append(t)
                point = p + t * delta - center
                angles[index].append(atan2(float(point[1]), float(point[0])) % (2 * pi))
        breaks = sorted(set(breaks))
        for low, high in zip(breaks[:-1], breaks[1:], strict=True):
            midpoint = p + (low + high) * 0.5 * delta
            if np.any(np.sum((centers - midpoint) ** 2, axis=1) < radii_squared):
                continue
            line_terms.append(0.5 * _cross(p + low * delta, p + high * delta))
    for first, second in combinations(range(len(radii)), 2):
        delta = centers[second] - centers[first]
        distance = float(np.linalg.norm(delta))
        r, s = float(radii[first]), float(radii[second])
        if distance == 0 or distance > r + s or distance < abs(r - s):
            continue
        direction = atan2(float(delta[1]), float(delta[0]))
        for index, radius, other_radius, angle in (
            (first, r, s, direction),
            (second, s, r, direction + pi),
        ):
            opening = acos(
                max(
                    -1.0,
                    min(
                        1.0,
                        (distance**2 + radius**2 - other_radius**2)
                        / (2 * distance * radius),
                    ),
                )
            )
            angles[index].extend(
                ((angle - opening) % (2 * pi), (angle + opening) % (2 * pi))
            )
    arc_terms = []
    for index, (center, radius) in enumerate(zip(centers, radii, strict=True)):
        breaks = sorted(set(angles[index]))
        others = np.arange(len(radii)) != index
        for low, high in zip(breaks[:-1], breaks[1:], strict=True):
            middle = (low + high) * 0.5
            point = center + radius * np.array([cos(middle), sin(middle)])
            if any(_cross(delta, point - p) < -tolerance for p, delta in edges):
                continue
            if np.any(
                np.sum((centers[others] - point) ** 2, axis=1)
                < radii_squared[others] - tolerance
            ):
                continue
            arc_terms.append(
                0.5
                * (
                    radius**2 * (high - low)
                    + radius * center[0] * (sin(high) - sin(low))
                    + radius * center[1] * (cos(low) - cos(high))
                )
            )
    area = fsum(line_terms) - fsum(arc_terms)
    if area < -10 * tolerance or area > polygon_area + 10 * tolerance:
        raise ArithmeticError("Disk-boundary integral exceeds physical area bounds")
    return max(0.0, min(float(area), polygon_area))


def _clip_rectangle(
    polygon: np.ndarray, low: np.ndarray, high: np.ndarray
) -> np.ndarray:
    for axis, boundary, sign in (
        (0, low[0], 1),
        (0, high[0], -1),
        (1, low[1], 1),
        (1, high[1], -1),
    ):
        if not len(polygon):
            break
        result = []
        previous = polygon[-1]
        previous_inside = sign * (previous[axis] - boundary) >= 0
        for point in polygon:
            inside = sign * (point[axis] - boundary) >= 0
            if inside != previous_inside:
                fraction = (boundary - previous[axis]) / (point[axis] - previous[axis])
                result.append(previous + fraction * (point - previous))
            if inside:
                result.append(point)
            previous, previous_inside = point, inside
        polygon = np.asarray(result, dtype=float).reshape((-1, 2))
    return polygon


def _tetrahedron_section(tetrahedron: np.ndarray, height: float) -> np.ndarray:
    points = []
    for first, second in combinations(tetrahedron, 2):
        low, high = sorted((float(first[2]), float(second[2])))
        if height < low or height > high:
            continue
        if first[2] == second[2]:
            if height == first[2]:
                points.extend((first[:2], second[:2]))
        else:
            fraction = (height - first[2]) / (second[2] - first[2])
            points.append(first[:2] + fraction * (second[:2] - first[:2]))
    if len(points) < 3:
        return np.empty((0, 2))
    polygon = np.unique(np.asarray(points), axis=0)
    center = polygon.mean(axis=0)
    return polygon[
        np.argsort(np.arctan2(polygon[:, 1] - center[1], polygon[:, 0] - center[0]))
    ]


def integrate_tetrahedron(
    tetrahedron: np.ndarray,
    centers: np.ndarray,
    radii: np.ndarray,
    *,
    epsabs: float,
    subdivisions: int = 32,
    enclosure: np.ndarray | None = None,
) -> dict:
    """Integrate outside-sphere cross sections in an explicit tetrahedron.

    Optional enclosure is a caller-justified conservative (low, high) XYZ box
    for the uncovered volume; an arbitrary box changes the physical domain.
    Quadrature error is an estimate, not a certified bound or an equivalence
    verdict. Inputs are bare values in one common caller-declared length unit.
    """
    tetrahedron, centers, radii = map(
        lambda x: np.asarray(x, dtype=float), (tetrahedron, centers, radii)
    )
    if (
        tetrahedron.shape != (4, 3)
        or radii.ndim != 1
        or centers.shape != (len(radii), 3)
    ):
        raise ValueError("Tetrahedron, sphere center and radius shapes differ")
    if not all(
        np.all(np.isfinite(value)) for value in (tetrahedron, centers, radii)
    ) or np.any(radii < 0):
        raise ValueError("Geometry must be finite and radii non-negative")
    if np.linalg.det(tetrahedron[1:] - tetrahedron[0]) == 0:
        raise ValueError("Tetrahedron is degenerate")
    if not np.isfinite(epsabs) or epsabs <= 0 or subdivisions < 1:
        raise ValueError("Positive tolerance and subdivisions are required")
    low, high = tetrahedron.min(axis=0), tetrahedron.max(axis=0)
    if enclosure is not None:
        enclosure = np.asarray(enclosure, dtype=float)
        if (
            enclosure.shape != (2, 3)
            or not np.all(np.isfinite(enclosure))
            or np.any(enclosure[0] >= enclosure[1])
        ):
            raise ValueError("Enclosure must be a finite, ordered (2, 3) box")
        low, high = np.maximum(low, enclosure[0]), np.minimum(high, enclosure[1])
        if np.any(low >= high):
            raise ValueError("Enclosure does not intersect the tetrahedron")
    origin = (low + high) * 0.5
    tetrahedron, centers, low, high = (
        tetrahedron - origin,
        centers - origin,
        low - origin,
        high - origin,
    )
    distances = np.maximum(np.maximum(low - centers, centers - high), 0.0)
    keep = np.sum(distances**2, axis=1) <= radii**2
    centers, radii = centers[keep], radii[keep]
    evaluations, positive_sections = 0, 0

    def integrand(height):
        nonlocal evaluations, positive_sections
        evaluations += 1
        polygon = _clip_rectangle(
            _tetrahedron_section(tetrahedron, height), low[:2], high[:2]
        )
        if len(polygon) < 3:
            return 0.0
        radius_squared = radii**2 - (height - centers[:, 2]) ** 2
        active = radius_squared > 0
        area = uncovered_polygon_area(
            polygon, centers[active, :2], np.sqrt(radius_squared[active])
        )
        positive_sections += int(area > 0)
        return area

    points = np.unique(
        np.concatenate(
            (
                np.linspace(low[2], high[2], subdivisions + 1),
                tetrahedron[:, 2],
                centers[:, 2] - radii,
                centers[:, 2] + radii,
            )
        )
    )
    points = points[(points > low[2]) & (points < high[2])]
    result = quad(
        integrand,
        low[2],
        high[2],
        points=points,
        epsabs=epsabs,
        epsrel=1e-11,
        limit=max(200, len(points) * 10),
        full_output=1,
    )
    value, error, info = result[:3]
    return dict(
        volume=float(value),
        estimated_absolute_error=float(error),
        evaluations=evaluations,
        positive_sections=positive_sections,
        subdivisions=int(subdivisions),
        quadrature_intervals=int(info["last"]),
        messages=list(result[3:]),
        error_bound_certified=False,
        enclosure_used=enclosure is not None,
        candidate_spheres=len(radii),
    )
