import unittest
import time
from TP.modules.Point import Point
from TP.modules.Triangulation import Triangulation

class TestTriangulationPerf(unittest.TestCase):
    def test_performance_petits_ensembles(self):
        # On crée 100 points d'où "petit ensemble"
        points = [Point(i, i) for i in range(100)]
        
        debut = time.time()
        Triangulation.depuis_points_eventail(points)
        fin = time.time()
        
        duree = fin - debut
        # On vérifie juste que la durée d'exécution est quasi-instantannée
        self.assertLess(duree, 0.1)

if __name__ == '__main__':
    unittest.main()
