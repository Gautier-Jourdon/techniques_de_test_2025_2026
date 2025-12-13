import struct
from typing import Iterable, List, Tuple
from TP.modules.Point import Point
from TP.modules.PointSet import PointSet

class Triangulation:
    def __init__(self, ensemble_points: PointSet = None, indices_triangles: List[Tuple[int, int, int]] = None):
        self.sommets = ensemble_points if ensemble_points else PointSet()
        self.triangles = indices_triangles if indices_triangles else []

    def ajouter_triangle(self, index1: int, index2: int, index3: int):
        taille = len(self.sommets)
        if not (0 <= index1 < taille and 0 <= index2 < taille and 0 <= index3 < taille):
            raise ValueError("Indices invalides")
        self.triangles.append((index1, index2, index3))

    def obtenir_triangles_points(self):
        resultat = []
        for i1, i2, i3 in self.triangles:
            p1 = self.sommets[i1]
            p2 = self.sommets[i2]
            p3 = self.sommets[i3]
            resultat.append((p1, p2, p3))
        return resultat

    def vers_octets(self) -> bytes:
        # 1. Sérialisation des points
        donnees = bytearray(self.sommets.vers_octets())
        
        # 2. Sérialisation des triangles
        donnees.extend(struct.pack("<I", len(self.triangles)))
        
        # Ajout des indices (3 entiers par triangle)
        for i1, i2, i3 in self.triangles:
            donnees.extend(struct.pack("<III", i1, i2, i3))
            
        return bytes(donnees)

    @classmethod
    def depuis_octets(cls, donnees: bytes) -> "Triangulation":
        # 1. PointSet
        if len(donnees) < 4:
            raise ValueError("Données trop courtes")
        
        (nb_points,) = struct.unpack_from("<I", donnees, 0)
        taille_pointset = 4 + nb_points * 8
        
        if len(donnees) < taille_pointset:
            raise ValueError("Données incomplètes pour les points")
            
        sommets = PointSet.depuis_octets(donnees[:taille_pointset])
        
        # 2. Triangles
        position = taille_pointset
        if len(donnees) < position + 4:
             raise ValueError("Données incomplètes pour le nombre de triangles")
             
        (nb_triangles,) = struct.unpack_from("<I", donnees, position)
        position += 4
        
        taille_attendue = position + nb_triangles * 12
        if len(donnees) != taille_attendue:
            raise ValueError("Taille des données incorrecte")
            
        triangles = []
        for _ in range(nb_triangles):
            indices = struct.unpack_from("<III", donnees, position)
            triangles.append(indices)
            position += 12
            
        return cls(sommets, triangles)

    @classmethod
    def depuis_points_eventail(cls, points: Iterable[Point]) -> "Triangulation":
        import math
        liste_points = list(points)
        
        if len(liste_points) < 3:
            return cls(PointSet(liste_points), [])

        # 1. Calcul du centre de gravité
        cx = sum(p.getX() for p in liste_points) / len(liste_points)
        cy = sum(p.getY() for p in liste_points) / len(liste_points)

        # 2. Tri angulaire pour ordonner les points
        def obtenir_angle(p):
            return math.atan2(p.getY() - cy, p.getX() - cx)
            
        liste_points.sort(key=obtenir_angle)

        # 3. Création des triangles en éventail
        ensemble = PointSet(liste_points)
        indices = []
        for i in range(1, len(liste_points) - 1):
            indices.append((0, i, i + 1))
            
        return cls(ensemble, indices)
