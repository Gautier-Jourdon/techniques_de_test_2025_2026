import unittest
import time
from TP.modules.Point import Point
from TP.modules.PointSet import PointSet

# Notre fonction test_perf_parsing_pointset vient créer un gros paquet de données (1000 points)
# On convertit ensuite ce pointset ps en binaire (en octets)
# Je précise, le test de performances vise à mesurerr la vitesse de transformation du binaire en Python, en gros.

class TestBinaryConversionPerf(unittest.TestCase):
    def test_perf_parsing_pointset(self):
        points = [Point(float(i), float(i)) for i in range(1000)]
        ps = PointSet(points)
        donnees = ps.vers_octets()
        
        debut = time.time()
        PointSet.depuis_octets(donnees)
        fin = time.time()
        
        self.assertLess(fin - debut, 0.1)

if __name__ == '__main__':
    unittest.main()
