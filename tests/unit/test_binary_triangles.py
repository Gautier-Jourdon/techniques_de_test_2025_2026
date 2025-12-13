import unittest
from TP.modules.Point import Point
from TP.modules.PointSet import PointSet
from TP.modules.Triangulation import Triangulation

class TestBinaryTriangles(unittest.TestCase):
    def test_serialization_triangles(self):
        # Vérifie l'écriture binaire d'une triangulation
        ps = PointSet([Point(0, 0), Point(1, 0), Point(0, 1)])
        tri = Triangulation(ps, [(0, 1, 2)])
        
        donnees = tri.vers_octets()
        
        # On vérifie juste qu'on peut relire ce qu'on a écrit (j'utilise cette structure dans tous mes tests de toute façon)
        tri2 = Triangulation.depuis_octets(donnees)
        self.assertEqual(len(tri2.triangles), 1)
        self.assertEqual(tri2.triangles[0], (0, 1, 2))

    def test_triangulation_vide(self):
        # Vérifie le cas sans triangles (juste des points)
        ps = PointSet([Point(0,0), Point(1,1)])
        tri = Triangulation(ps, [])
        donnees = tri.vers_octets()
        
        tri2 = Triangulation.depuis_octets(donnees)
        self.assertEqual(len(tri2.triangles), 0)
        self.assertEqual(len(tri2.sommets), 2)

    def test_indices_invalides(self):
        # Vérifie qu'on ne peut pas créer un triangle avec des indices inexistants (j'utilise qu'un seul point dans ce but)
        ps = PointSet([Point(0,0)])
        tri = Triangulation(ps, [])
        
        # Essayer d'ajouter un triangle utilisant l'index 1 (qui n'existe pas)
        with self.assertRaises(ValueError):
            tri.ajouter_triangle(0, 1, 0)

    def test_donnees_corrompues(self):
        # Vérifie que la lecture plante si les données sont incomplètes
        ps = PointSet([Point(0,0), Point(1,0), Point(0,1)])
        tri = Triangulation(ps, [(0, 1, 2)])
        donnees = tri.vers_octets()
        
        # On enlève le dernier octet
        donnees_coupees = donnees[:-1]
        
        with self.assertRaises(ValueError):
            Triangulation.depuis_octets(donnees_coupees)

    def test_indices_doublons_triangle(self):
        # Un triangle "plat" (sommets identiques) est valide techniquement
        # On vérifie juste que ça ne plante pas
        ps = PointSet([Point(0,0), Point(1,1)])
        tri = Triangulation(ps, [(0, 0, 1)])
        donnees = tri.vers_octets()
        tri2 = Triangulation.depuis_octets(donnees)
        self.assertEqual(tri2.triangles[0], (0, 0, 1))

    def test_limites_indices(self):
        # Vérifie que les indices élevés passent bien (format 4 octets)
        ps = PointSet([Point(0,0)] * 300) # 300 points
        tri = Triangulation(ps, [(0, 1, 299)])
        donnees = tri.vers_octets()
        tri2 = Triangulation.depuis_octets(donnees)
        self.assertEqual(tri2.triangles[0], (0, 1, 299))

if __name__ == '__main__':
    unittest.main()
