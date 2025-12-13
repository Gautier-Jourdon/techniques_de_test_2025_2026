import unittest
from TP.modules.Point import Point
from TP.modules.Triangulation import Triangulation

class TestTriangulationAlgorithm(unittest.TestCase):
    def test_triangle_simple(self):
        # Cas basique : 3 points forment 1 triangle
        pts = [Point(0,0), Point(1,0), Point(0,1)]
        tri = Triangulation.depuis_points_eventail(pts)
        self.assertEqual(len(tri.triangles), 1)

    def test_carre(self):
        # Un carré (4 points) doit donner 2 triangles
        pts = [Point(0,0), Point(1,0), Point(1,1), Point(0,1)]
        tri = Triangulation.depuis_points_eventail(pts)
        self.assertEqual(len(tri.triangles), 2)

    def test_points_colineaires(self):
        # 3 points alignés créent un triangle "plat" (c'est valide techniquement, pas très utile mais ça fonctionne)
        pts = [Point(0,0), Point(1,0), Point(2,0)]
        tri = Triangulation.depuis_points_eventail(pts)
        self.assertEqual(len(tri.triangles), 1)
        
    def test_points_doublons(self):
        # Les doublons créent des triangles de surface nulle
        pts = [Point(0,0), Point(0,0), Point(1,1)]
        tri = Triangulation.depuis_points_eventail(pts)
        self.assertEqual(len(tri.triangles), 1)

    def test_grand_nombre_points(self):
        # Vérifie que l'algo tient la route avec 50 points
        pts = [Point(i, i) for i in range(50)]
        tri = Triangulation.depuis_points_eventail(pts)
        self.assertEqual(len(tri.triangles), 48)

    def test_points_tres_proches(self):
        # Vérifie la robustesse avec des points quasi-identiques
        pts = [Point(0, 0), Point(1e-10, 0), Point(0, 1e-10)]
        tri = Triangulation.depuis_points_eventail(pts)
        self.assertEqual(len(tri.triangles), 1)

    def test_coordonnees_extremes(self):
        # Vérifie que les très grands nombres ne cassent rien
        grand = 1e30
        pts = [Point(0, 0), Point(grand, 0), Point(0, grand)]
        tri = Triangulation.depuis_points_eventail(pts)
        self.assertEqual(len(tri.triangles), 1)

if __name__ == '__main__':
    unittest.main()
