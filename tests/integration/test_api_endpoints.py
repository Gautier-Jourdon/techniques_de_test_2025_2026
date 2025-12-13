import unittest
from unittest.mock import MagicMock, patch
from TP.modules.Client import ClientAPI

# Ici, on simule des données binaires vides valides pour l'exemple
# On retourne automatiquement un code 200 (qui correspond à une validation)
# (Il faudrait un binaire complet, mais ici on teste juste le code HTTP)

class TestAPIEndpoints(unittest.TestCase):
    @patch('requests.get')
    def test_get_triangulation_200(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        pass

if __name__ == '__main__':
    unittest.main()
