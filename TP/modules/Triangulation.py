"""Triangulation
`Triangles` représente un ensemble de triangles, dont les sommets sont des
points dans un espace à 2 dimensions, un `PointSet` donc. Il est donc assez
logique que la représentation de `Triangles` soit dérivée de celle de `PointSet`.

La représentation binaire de `Triangles` est donc en deux parties:
- La première partie décrit les sommets et est strictement la même que pour un `PointSet`
- La seconde partie décrit les triangles à proprement parler et se compose de:
  - 4 bytes (un `unsigned long`) qui représente le nombre de triangles
  - 3 x 4 x {nombre de triangles} bytes, pour chaque triangle il y a donc 12 bytes,
    chaque 4 bytes sont un `unsigned long` qui référence l'indice d'un sommet du
    triangle dans le `PointSet`.
"""

from typing import Iterable, Tuple, List
import struct
from Point import Point

Triangle = Tuple[Point, Point, Point]

class TriangleIndices:
    """Triangle référencé par indices de sommets."""
    def __init__(self, i1: int, i2: int, i3: int):
        self._indices = (i1, i2, i3)
    def get_indices(self) -> Tuple[int, int, int]:  # attendu par client_test
        return self._indices


class Triangulation:
	"""Conteneur de triangles (3 sommets) ou résultat de triangulation.

	Deux modes:
	 - stockage direct des triangles (liste de triplets de Point)
	 - résultat décodé via from_binary: attributs vertices (PointSet-like) et triangles (indices)
	"""

	_COUNT_STRUCT = struct.Struct("<I")
	_POINT_STRUCT = struct.Struct("<ff")

	def __init__(self, triangles: Iterable[Triangle] | None = None):
		self._liste_triangles: list[Triangle] = []
		self.vertices = None            # sera un PointSet pour le résultat binaire
		self.triangles: List[TriangleIndices] | None = None  # triangles par indices
		if triangles:
			for tri in triangles:
				self.ajouter_triangle(*tri)

	# --- Gestion ---
	def ajouter_triangle(self, a: Point, b: Point, c: Point) -> None:
		self._liste_triangles.append((a, b, c))

	def retirer_triangle(self, triangle: Triangle) -> None:
		try:
			self._liste_triangles.remove(triangle)
		except ValueError as e:
			raise ValueError("Triangle absent") from e

	def vider(self) -> None:
		self._liste_triangles.clear()

	def __len__(self) -> int:
		return len(self._liste_triangles)

	def __iter__(self):
		return iter(self._liste_triangles)

	def __getitem__(self, idx: int) -> Triangle:
		return self._liste_triangles[idx]

	def en_liste(self) -> list[Triangle]:
		return list(self._liste_triangles)

	# --- Création simple à partir d'un PointSet (trouvé sur le web) ---
	@classmethod
	def depuis_ensemble_eventail(cls, ensemble_points) -> "Triangulation":
		"""Triangulation éventail naïve à partir d'un ensemble de points."""
		pts = list(ensemble_points)
		if len(pts) < 3:
			return cls()
		p0 = pts[0]
		triangles = []
		for i in range(1, len(pts) - 1):
			triangles.append((p0, pts[i], pts[i + 1]))
		return cls(triangles)

	# --- Calcul de l'Aire du triangle ---
	@staticmethod
	def _aire_triangle(tri: Triangle) -> float:
		a, b, c = tri
		x1, y1 = a.get_x(), a.get_y()
		x2, y2 = b.get_x(), b.get_y()
		x3, y3 = c.get_x(), c.get_y()
		return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) * 0.5)

	def aire_totale(self) -> float:
		return sum(self._aire_triangle(t) for t in self._liste_triangles)

	# --- Sérialisation des données en bynaires pour le stockage facile ---
	def to_bytes(self) -> bytes:
		"""Ancien format interne (non indices)."""
		count = len(self._liste_triangles)
		out = bytearray(self._COUNT_STRUCT.pack(count))
		for a, b, c in self._liste_triangles:
			out.extend(self._POINT_STRUCT.pack(a.get_x(), a.get_y()))
			out.extend(self._POINT_STRUCT.pack(b.get_x(), b.get_y()))
			out.extend(self._POINT_STRUCT.pack(c.get_x(), c.get_y()))
		return bytes(out)
    # --- ça aussi ---
	@classmethod
	def from_bytes(cls, data: bytes) -> "Triangulation":
		"""Décodage de l'ancien format (coordonnées répétées)."""
		if len(data) < cls._COUNT_STRUCT.size:
			raise ValueError("Données trop courtes")
		(count,) = cls._COUNT_STRUCT.unpack_from(data, 0)
		tri_size = 3 * cls._POINT_STRUCT.size
		attendu = cls._COUNT_STRUCT.size + count * tri_size
		if len(data) != attendu:
			raise ValueError("Longueur incohérente")
		pos = cls._COUNT_STRUCT.size
		triangles: list[Triangle] = []
		for _ in range(count):
			pts: list[Point] = []
			for _ in range(3):
				x, y = cls._POINT_STRUCT.unpack_from(data, pos)
				pts.append(Point(x, y))
				pos += cls._POINT_STRUCT.size
			triangles.append((pts[0], pts[1], pts[2]))
		return cls(triangles)

	# --- Nouveau format (Partie sommets puis indices) ---
	@classmethod
	def from_binary(cls, data: bytes) -> "Triangulation":
		"""Décodage format vertices+indices conforme au YAML."""
		# Partie 1 : sommets
		if len(data) < cls._COUNT_STRUCT.size:
			raise ValueError("Données trop courtes")
		(n_vertices,) = cls._COUNT_STRUCT.unpack_from(data, 0)
		vertices_section = cls._COUNT_STRUCT.size + n_vertices * cls._POINT_STRUCT.size
		if len(data) < vertices_section + cls._COUNT_STRUCT.size:
			raise ValueError("Données incomplètes pour les triangles")
		# Charger les sommets
		pos = cls._COUNT_STRUCT.size
		verts: list[Point] = []
		for _ in range(n_vertices):
			x, y = cls._POINT_STRUCT.unpack_from(data, pos)
			verts.append(Point(x, y))
			pos += cls._POINT_STRUCT.size
		# Partie 2 : triangles par indices
		(n_tris,) = cls._COUNT_STRUCT.unpack_from(data, pos)
		pos += cls._COUNT_STRUCT.size
		triangles_indices: List[TriangleIndices] = []
		index_struct = cls._COUNT_STRUCT  # <I
		expected_total = vertices_section + cls._COUNT_STRUCT.size + n_tris * 3 * index_struct.size
		if len(data) != expected_total:
			raise ValueError("Longueur binaire incohérente")
		for _ in range(n_tris):
			i1, = index_struct.unpack_from(data, pos); pos += index_struct.size
			i2, = index_struct.unpack_from(data, pos); pos += index_struct.size
			i3, = index_struct.unpack_from(data, pos); pos += index_struct.size
			triangles_indices.append(TriangleIndices(i1, i2, i3))
		obj = cls()
		from TP.modules.PointSet import PointSet  # import local pour éviter cycle
		obj.vertices = PointSet(verts)
		obj.triangles = triangles_indices
		return obj

	def to_binary(self) -> bytes:
		"""Encode format vertices + indices (fan si nécessaire)."""
		from TP.modules.PointSet import PointSet
		if self.vertices is not None and self.triangles is not None:
			verts = self.vertices
			tris = self.triangles
		else:
			# Construire fan sur triangles existants si pas déjà indices
			all_points: list[Point] = []
			for tri in self._liste_triangles:
				for p in tri:
					if p not in all_points:
						all_points.append(p)
			verts = PointSet(all_points)
			# Fan naive : utiliser order d'insertion
			if len(all_points) < 3:
				tris = []
			else:
				p0_index = 0
				tris = [TriangleIndices(p0_index, i, i + 1) for i in range(1, len(all_points) - 1)]
		# Partie sommets
		out = bytearray(self._COUNT_STRUCT.pack(len(verts)))
		for p in verts:
			out.extend(self._POINT_STRUCT.pack(p.get_x(), p.get_y()))
		# Partie triangles
		out.extend(self._COUNT_STRUCT.pack(len(tris)))
		for t in tris:
			i1, i2, i3 = t.get_indices()
			out.extend(self._COUNT_STRUCT.pack(i1))
			out.extend(self._COUNT_STRUCT.pack(i2))
			out.extend(self._COUNT_STRUCT.pack(i3))
		return bytes(out)

	def save(self, file_path: str) -> None:
		with open(file_path, "wb") as f:
			f.write(self.to_bytes())

	@classmethod
	def load(cls, file_path: str) -> "Triangulation":
		with open(file_path, "rb") as f:
			return cls.from_bytes(f.read())

	def __repr__(self) -> str:
		return f"Triangulation({len(self)} triangles)"

	def __str__(self) -> str:
		return "; ".join(
			f"({a.get_x()},{a.get_y()})-({b.get_x()},{b.get_y()})-({c.get_x()},{c.get_y()})"
			for a, b, c in self._liste_triangles
		)

__all__ = ["Triangulation", "Triangle"]
