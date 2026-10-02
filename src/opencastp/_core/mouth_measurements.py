"""Analytical measures over alpha-complex mouth triangles and their arcs."""

from dataclasses import dataclass
from math import acos, pi, sin, sqrt
from typing import Literal

import numpy as np

from .volbl import _edge_in_complex


@dataclass(frozen=True, slots=True)
class MouthMeasurement:
    """Store the two mouth area/perimeter models in geometry length units."""

    area_sa: float
    area_ms: float
    perimeter_sa: float
    perimeter_ms: float


def _acos(value: float) -> float:
    return acos(max(-1.0, min(1.0, value)))


def triangle_mouth_measurements(
    points: np.ndarray,
    expanded_radii: np.ndarray,
    probe_radius: float,
    complex_edges: tuple[bool, bool, bool],
    *,
    policy: Literal["signed", "castp3"] = "signed",
) -> MouthMeasurement:
    """Integrate sectors and overlaps in one oriented-independent mouth face.

    Alpha membership controls which pair terms belong to this face. Geometric
    disk overlap alone would include terms outside the region's dual complex.
    Molecular arcs use the bare atomic radii and the tangent solvent circle.
    When that circle crosses an edge, its out-of-triangle cap is excluded from
    area. Perimeter retains the analytical boundary-arc convention. The
    signed projection model and the reconstructed unsigned CASTp3 model are
    explicit alternatives; neither policy changes region geometry or radii.
    """
    if policy not in ("signed", "castp3"):
        raise ValueError("Unknown mouth measurement policy")
    points = np.asarray(points, dtype=float)
    radii = np.asarray(expanded_radii, dtype=float)
    probe = float(probe_radius)
    if points.shape != (3, 3) or radii.shape != (3,):
        raise ValueError("One triangle and three expanded radii are required")
    if not np.all(np.isfinite(points)) or not np.all(np.isfinite(radii)):
        raise ValueError("Mouth geometry must be finite")
    if not np.isfinite(probe) or probe < 0 or np.any(radii <= probe):
        raise ValueError("Atomic radii must be positive and probe non-negative")
    area = float(
        np.linalg.norm(np.cross(points[1] - points[0], points[2] - points[0])) / 2
    )
    if area == 0:
        raise ValueError("Mouth triangle is degenerate")
    atomic = radii - probe
    area_sa = area_ms = area
    perimeter_sa = perimeter_ms = 0.0
    for i, j, k in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
        first, second = points[j] - points[i], points[k] - points[i]
        angle = _acos(
            float(
                np.dot(first, second) / (np.linalg.norm(first) * np.linalg.norm(second))
            )
        )
        area_sa -= 0.5 * angle * radii[i] ** 2
        area_ms -= 0.5 * angle * atomic[i] ** 2
        perimeter_sa += angle * radii[i]
        perimeter_ms += angle * atomic[i]
    for (i, j), in_complex in zip(((0, 1), (0, 2), (1, 2)), complex_edges, strict=True):
        if not in_complex:
            continue
        distance = float(np.linalg.norm(points[j] - points[i]))
        first, second = float(radii[i]), float(radii[j])
        first_atomic, second_atomic = float(atomic[i]), float(atomic[j])
        bisector = (first**2 - second**2 + distance**2) / (2 * distance)
        height = sqrt(max(0.0, first**2 - bisector**2))
        first_projection, second_projection = bisector, distance - bisector
        if policy == "castp3":
            # The archived-server convention sums unsigned circular segments.
            # Preserve its behavior when a bisector lies beyond either center;
            # signed geometry remains an independent, explicit choice.
            first_projection = abs(first_projection)
            second_projection = abs(second_projection)
        first_angle = _acos(first_projection / first)
        second_angle = _acos(second_projection / second)
        segment_distance = first_projection + second_projection
        probe_angle = pi - first_angle - second_angle
        area_sa += 0.5 * (
            first**2 * first_angle
            + second**2 * second_angle
            - segment_distance * height
        )
        perimeter_sa -= first * first_angle + second * second_angle
        # The tangent quadrilateral joins the atom centers and solvent-contact
        # points. Subtract it, then restore the solvent circular segment.
        polygon_area = (
            0.5
            * segment_distance
            * height
            * (
                first_atomic / first
                + second_atomic / second
                - first_atomic * second_atomic / (first * second)
            )
        )
        area_ms += (
            0.5 * (first_atomic**2 * first_angle + second_atomic**2 * second_angle)
            - polygon_area
            + 0.5 * probe**2 * (probe_angle - sin(probe_angle))
        )
        perimeter_ms += (
            probe * probe_angle
            - first_atomic * first_angle
            - second_atomic * second_angle
        )
        if height < probe:
            area_ms -= probe**2 * _acos(height / probe) - height * sqrt(
                probe**2 - height**2
            )
    return MouthMeasurement(
        float(area_sa), float(area_ms), float(perimeter_sa), float(perimeter_ms)
    )


def mouth_measurements(
    geometry,
    faces: list[tuple[int, int, int]],
    probe_radius: float,
    *,
    policy: Literal["signed", "castp3"] = "signed",
) -> MouthMeasurement:
    """Sum analytical contributions over one topological mouth's triangles."""
    values = np.zeros(4)
    for face in faces:
        indices = list(face)
        edges = tuple(
            _edge_in_complex(
                geometry, int(face[i]), int(face[j]), int(geometry.base_rank)
            )
            for i, j in ((0, 1), (0, 2), (1, 2))
        )
        item = triangle_mouth_measurements(
            geometry.atom_coordinates[indices],
            geometry.atom_radii[indices],
            probe_radius,
            edges,
            policy=policy,
        )
        values += item.area_sa, item.area_ms, item.perimeter_sa, item.perimeter_ms
    return MouthMeasurement(*map(float, values))
