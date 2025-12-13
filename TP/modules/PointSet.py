import struct
from typing import Iterable, List
from TP.modules.Point import Point

class PointSet:
    def __init__(self, points: Iterable[Point] = None):
        self.points = []
        if points:
            for p in points:
                self.ajouter(p)

    def ajouter(self, point: Point):
        if not isinstance(point, Point):
            raise TypeError("Il faut ajouter un objet Point")
        self.points.append(point)

    def retirer(self, point: Point):
        if point in self.points:
            self.points.remove(point)
        else:
            raise ValueError("Point introuvable")

    def vider(self):
        self.points.clear()

    def taille(self):
        return len(self.points)

    def vers_octets(self) -> bytes:
        # Format binaire : [Nb Points (4o)] + [Point (8o)]...
        nb_points = len(self.points)
        # 'I' = unsigned int, 'f' = float, '<' = little-endian
        donnees = bytearray(struct.pack("<I", nb_points))
        
        for p in self.points:
            donnees.extend(struct.pack("<ff", p.getX(), p.getY()))
            
        return bytes(donnees)

    @classmethod
    def depuis_octets(cls, donnees: bytes) -> "PointSet":
        if len(donnees) < 4:
            raise ValueError("Données trop courtes")
            
        (nb_points,) = struct.unpack_from("<I", donnees, 0)
        
        taille_attendue = 4 + nb_points * 8
        if len(donnees) != taille_attendue:
            raise ValueError("Taille des données incorrecte")
            
        points = []
        position = 4
        for _ in range(nb_points):
            x, y = struct.unpack_from("<ff", donnees, position)
            points.append(Point(x, y))
            position += 8
            
        return cls(points)

    # Méthodes spéciales pour faciliter l'usage (len, iter, index)
    def __len__(self):
        return len(self.points)

    def __iter__(self):
        return iter(self.points)

    def __getitem__(self, index):
        return self.points[index]
