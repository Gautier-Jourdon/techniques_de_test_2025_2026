import unittest
from TP.modules.Point import Point
from TP.modules.PointSet import PointSet

# Aidé par Gemini et forums web

class TestBinaryPointSet(unittest.TestCase):
    def test_parsing_valide(self):
        # Vérifie la lecture d'un PointSet binaire simple
        donnees = bytes.fromhex("010000000000803F00000040")
        ps = PointSet.depuis_octets(donnees)
        
        self.assertEqual(len(ps), 1)
        self.assertEqual(ps[0].getX(), 1.0)

    def test_serialization(self):
        # Vérifie l'écriture binaire d'un PointSet
        ps = PointSet([Point(1.0, 2.0)])
        donnees = ps.vers_octets()
        
        attendu = bytes.fromhex("010000000000803F00000040")
        self.assertEqual(donnees, attendu)

    def test_ensemble_vide(self):
        # Vérifie le cas d'un ensemble sans points
        ps = PointSet([])
        donnees = ps.vers_octets()
        self.assertEqual(donnees, bytes.fromhex("00000000"))
        
        ps2 = PointSet.depuis_octets(donnees)
        self.assertEqual(len(ps2), 0)

    def test_coordonnees_negatives(self):
        # Vérifie que les nombres négatifs passent bien
        ps = PointSet([Point(-1.0, -2.0)])
        donnees = ps.vers_octets()
        ps2 = PointSet.depuis_octets(donnees)
        self.assertEqual(ps2[0].getX(), -1.0)
        self.assertEqual(ps2[0].getY(), -2.0)

    def test_donnees_invalides_taille(self):
        # Vérifie que ça plante si les données sont coupées
        donnees = bytes.fromhex("010000000000803F0000") 
        with self.assertRaises(ValueError):
            PointSet.depuis_octets(donnees)

    def test_donnees_invalides_compteur(self):
        # Vérifie que ça plante si le nombre de points annoncé est faux
        donnees = bytes.fromhex("050000000000803F00000040")
        with self.assertRaises(ValueError):
            PointSet.depuis_octets(donnees)

    def test_precision_flottante(self):
        # Vérifie la précision des nombres à virgule
        valeur_precise = 1.2345678
        ps = PointSet([Point(valeur_precise, -valeur_precise)])
        donnees = ps.vers_octets()
        ps2 = PointSet.depuis_octets(donnees)
        
        self.assertAlmostEqual(ps2[0].getX(), valeur_precise, places=6)
        self.assertAlmostEqual(ps2[0].getY(), -valeur_precise, places=6)

    def test_grand_volume_donnees(self):
        # Vérifie que ça tient la charge avec 1000 points
        nb_points = 1000
        ps = PointSet([Point(float(i), float(i)) for i in range(nb_points)])
        donnees = ps.vers_octets()
        ps2 = PointSet.depuis_octets(donnees)
        self.assertEqual(len(ps2), nb_points)
        self.assertEqual(ps2[999].getX(), 999.0)

if __name__ == '__main__':
    unittest.main()
