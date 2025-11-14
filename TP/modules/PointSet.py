"""PointSet
`PointSet` est un ensemble de points dans un espace en 2D, chaque point de
l'ensemble se résume donc à 2 coordonnées, X et Y.
La représentation de ces données est assez simple:
- Les 4 premiers bytes représentent un `unsigned long` donnant le nombre de
points dans l'ensemble
- Les bytes suivants représentent les points, avec pour chaque point 8 bytes.
Les 4 premiers bytes sont la coordonnée X (un `float`) et les 4 bytes suivant
la coordonnée Y (un `float` aussi).
"""

from typing import Iterable, List
import struct
from Point import Point


class PointSet:
    _COUNT_STRUCT = struct.Struct("<I")
    _POINT_STRUCT = struct.Struct("<ff")

    def __init__(self, points: Iterable[Point] | None = None):
        self._points: List[Point] = []
        if points:
            for p in points:
                self.add(p)

    # --- Méthodes de collection ---
    def add(self, point: Point) -> None:
        """Ajoute un point à l'ensemble.

        Raises:
            TypeError: si l'objet n'est pas une instance de Point.
        """
        if not isinstance(point, Point):
            raise TypeError("Seuls des objets Point peuvent être ajoutés")
        self._points.append(point)

    def remove(self, point: Point) -> None:
        """Retire un point existant. ValueError si absent."""
        try:
            self._points.remove(point)
        except ValueError as e:
            raise ValueError("Le point n'est pas présent dans l'ensemble") from e

    def clear(self) -> None:
        """Vide l'ensemble."""
        self._points.clear()

    def __len__(self) -> int:  # permet len(point_set)
        return len(self._points)

    def size(self) -> int:
        """Nombre de points."""
        return len(self._points)

    def __iter__(self):  # iteration sur les points
        return iter(self._points)

    def __getitem__(self, idx: int) -> Point:
        return self._points[idx]

    def __contains__(self, item: Point) -> bool:
        return item in self._points

    def to_list(self) -> List[Point]:
        return list(self._points)

    # --- Sérialisation binaire ---
    def to_bytes(self) -> bytes:
        count = len(self._points)
        out = bytearray(self._COUNT_STRUCT.pack(count))
        for p in self._points:
            out.extend(self._POINT_STRUCT.pack(float(p.get_x()), float(p.get_y())))
        return bytes(out)

    @classmethod
    def from_bytes(cls, data: bytes) -> "PointSet":
        if len(data) < cls._COUNT_STRUCT.size:
            raise ValueError("Données trop courtes")
        (count,) = cls._COUNT_STRUCT.unpack_from(data, 0)
        attendu = cls._COUNT_STRUCT.size + count * cls._POINT_STRUCT.size
        if len(data) != attendu:
            raise ValueError("Longueur incohérente avec le nombre de points")
        points: List[Point] = []
        pos = cls._COUNT_STRUCT.size
        for _ in range(count):
            x, y = cls._POINT_STRUCT.unpack_from(data, pos)
            points.append(Point(x, y))
            pos += cls._POINT_STRUCT.size
        return cls(points)

    # Alias attendu par client_test.py
    @classmethod
    def from_binary(cls, data: bytes) -> "PointSet":
        return cls.from_bytes(data)

    def save(self, file_path: str) -> None:
        with open(file_path, "wb") as f:
            f.write(self.to_bytes())

    @classmethod
    def load(cls, file_path: str) -> "PointSet":
        with open(file_path, "rb") as f:
            return cls.from_bytes(f.read())

    # --- Utilitaire simple ---
    def bounding_box(self) -> tuple[float, float, float, float] | None:
        if not self._points:
            return None
        xs = [p.get_x() for p in self._points]
        ys = [p.get_y() for p in self._points]
        return min(xs), min(ys), max(xs), max(ys)

    def __repr__(self) -> str:  # aide au debug
        return f"PointSet({len(self)} points)"

    def __str__(self) -> str:
        return ", ".join(f"({p.get_x()},{p.get_y()})" for p in self._points)


__all__ = ["PointSet"]