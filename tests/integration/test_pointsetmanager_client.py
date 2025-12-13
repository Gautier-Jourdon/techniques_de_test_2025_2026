import unittest
import requests
from unittest.mock import MagicMock, patch
from TP.modules.Point import Point
from TP.modules.PointSet import PointSet
from TP.modules.Client import ClientAPI

class TestPointSetManagerClient(unittest.TestCase):
    def setUp(self):
        self.client = ClientAPI()
        self.ps = PointSet([Point(0,0), Point(1,1)])

    @patch('requests.post')
    def test_enregistrement_reussi(self, mock_post):
        # Simule une réponse positive du serveur (201 Created)
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "pointSetId": "123"
        }
        mock_post.return_value = mock_response

        id_recu = self.client.enregistrer_ensemble(self.ps)
        self.assertEqual(id_recu, "123")

    @patch('requests.post')
    def test_echec_connexion(self, mock_post):
        # Simule une erreur interne du serveur (500)
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            self.client.enregistrer_ensemble(self.ps)

    @patch('requests.get')
    def test_recuperer_ensemble_404(self, mock_get):
        # Simule un ensemble non trouvé (404)
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as cm:
            self.client.recuperer_ensemble("999")
        self.assertIn("HTTP 404", str(cm.exception))

    @patch('requests.get')
    def test_recuperer_triangulation_erreur_serveur(self, mock_get):
        # Simule une erreur lors de la triangulation
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as cm:
            self.client.recuperer_triangulation("123")
        self.assertIn("HTTP 500", str(cm.exception))

    @patch('requests.get')
    def test_timeout(self, mock_get):
        # Simule un timeout réseau
        mock_get.side_effect = requests.exceptions.Timeout
        
        with self.assertRaises(requests.exceptions.Timeout):
            self.client.recuperer_ensemble("123")

    @patch('requests.get')
    def test_reponse_malformee(self, mock_get):
        # Simule une réponse JSON invalide du serveur
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Le contenu n'est pas un PointSet binaire valide
        mock_response.content = b"ceci n'est pas un pointset"
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError):
            self.client.recuperer_ensemble("123")

    @patch('requests.get')
    def test_service_indisponible_503(self, mock_get):
        # Simule un service indisponible
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception) as cm:
            self.client.recuperer_ensemble("123")
        self.assertIn("HTTP 503", str(cm.exception))

    @patch('requests.post')
    def test_uuid_invalide_400(self, mock_post):
        # Simule une requête invalide (400 Bad Request)
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "message": "Format invalide"
        }
        mock_post.return_value = mock_response
        
        with self.assertRaises(Exception) as cm:
            self.client.enregistrer_ensemble(self.ps)
        self.assertIn("HTTP 400", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
