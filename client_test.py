"""
Client simple pour tester les APIs PointSetManager et Triangulator.
"""

import requests
import json
from Point import Point
from TP.modules.PointSet import PointSet
from TP.modules.Triangulation import Triangulation


class APIClient:
    """Client pour les APIs PointSetManager et Triangulator."""
    
    def __init__(self, manager_url="http://127.0.0.1:5000", triangulator_url="http://127.0.0.1:5001"):
        """
        Initialise le client.
        
        Args:
            manager_url: URL du PointSetManager
            triangulator_url: URL du Triangulator
        """
        self.manager_url = manager_url.rstrip('/')
        self.triangulator_url = triangulator_url.rstrip('/')
    
    def register_point_set(self, point_set: PointSet) -> str:
        """
        Enregistre un PointSet et retourne son ID.
        
        Args:
            point_set: PointSet à enregistrer
            
        Returns:
            ID du PointSet enregistré
            
        Raises:
            Exception: En cas d'erreur
        """
        binary_data = point_set.to_bytes()
        
        response = requests.post(
            f"{self.manager_url}/pointset",
            data=binary_data,
            headers={"Content-Type": "application/octet-stream"}
        )
        
        if response.status_code == 201:
            result = response.json()
            return result["pointSetId"]
        else:
            error_msg = f"HTTP {response.status_code}"
            try:
                error_data = response.json()
                error_msg += f": {error_data.get('message', 'Unknown error')}"
            except:
                error_msg += f": {response.text}"
            raise Exception(f"Failed to register PointSet: {error_msg}")
    
    def get_point_set(self, point_set_id: str) -> PointSet:
        """
        Récupère un PointSet par son ID.
        
        Args:
            point_set_id: ID du PointSet
            
        Returns:
            PointSet récupéré
            
        Raises:
            Exception: En cas d'erreur
        """
        response = requests.get(f"{self.manager_url}/pointset/{point_set_id}")
        
        if response.status_code == 200:
            binary_data = response.content
            return PointSet.from_binary(binary_data)
        else:
            error_msg = f"HTTP {response.status_code}"
            try:
                error_data = response.json()
                error_msg += f": {error_data.get('message', 'Unknown error')}"
            except:
                error_msg += f": {response.text}"
            raise Exception(f"Failed to get PointSet: {error_msg}")
    
    def get_triangulation(self, point_set_id: str) -> Triangulation:
        """
        Calcule la triangulation d'un PointSet.
        
        Args:
            point_set_id: ID du PointSet
            
        Returns:
            Structure Triangles avec la triangulation
            
        Raises:
            Exception: En cas d'erreur
        """
        response = requests.get(f"{self.triangulator_url}/triangulation/{point_set_id}")
        
        if response.status_code == 200:
            binary_data = response.content
            return Triangulation.from_binary(binary_data)
        else:
            error_msg = f"HTTP {response.status_code}"
            try:
                error_data = response.json()
                error_msg += f": {error_data.get('message', 'Unknown error')}"
            except:
                error_msg += f": {response.text}"
            raise Exception(f"Failed to get triangulation: {error_msg}")

def test_workflow():
    """Test du workflow complet."""
    print("=== Test du workflow complet ===")
    
    client = APIClient()
    
    try:
        # 1. Créer un PointSet de test
        points = [
            Point(0.0, 0.0),
            Point(2.0, 0.0),
            Point(1.0, 2.0),
            Point(3.0, 1.0),
            Point(0.5, 1.5)
        ]
        point_set = PointSet(points)
        print(f"1. PointSet créé avec {point_set.__len__()} points")
        
        # 2. Enregistrer le PointSet
        point_set_id = client.register_point_set(point_set)
        print(f"2. PointSet enregistré avec ID: {point_set_id}")
        
        # 3. Récupérer le PointSet
        retrieved_point_set = client.get_point_set(point_set_id)
        print(f"3. PointSet récupéré avec {retrieved_point_set.__len__()} points")
        
        # Vérifier l'égalité
        if point_set == retrieved_point_set:
            print("   ✓ PointSet récupéré identique à l'original")
        else:
            print("   ✗ PointSet récupéré différent de l'original")
        
        # 4. Calculer la triangulation
        triangulation = client.get_triangulation(point_set_id)
        print(f"4. Triangulation calculée:")
        print(f"   - {triangulation.vertices.size()} sommets")
        print(f"   - {len(triangulation.triangles)} triangles")
        
        # Afficher les triangles
        for i, triangle in enumerate(triangulation.triangles):
            indices = triangle.get_indices()
            vertices = [triangulation.vertices.get_point(idx) for idx in indices]
            coords = [(v.get_x(), v.get_y()) for v in vertices]
            print(f"   Triangle {i}: indices {indices} -> {coords}")
        
        print("=== Test réussi ! ===")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_error_cases():
    """Test des cas d'erreur."""
    print("\n=== Test des cas d'erreur ===")
    
    client = APIClient()
    
    # Test 1: PointSet inexistant
    try:
        fake_id = "00000000-0000-0000-0000-000000000000"
        client.get_point_set(fake_id)
        print("❌ Erreur: devrait avoir échoué pour ID inexistant")
    except Exception as e:
        print(f"✓ Erreur attendue pour ID inexistant: {e}")
    
    # Test 2: UUID invalide
    try:
        invalid_id = "invalid-uuid"
        client.get_point_set(invalid_id)
        print("❌ Erreur: devrait avoir échoué pour UUID invalide")
    except Exception as e:
        print(f"✓ Erreur attendue pour UUID invalide: {e}")
    
    # Test 3: Triangulation d'un PointSet inexistant
    try:
        fake_id = "00000000-0000-0000-0000-000000000000"
        client.get_triangulation(fake_id)
        print("❌ Erreur: devrait avoir échoué pour triangulation inexistante")
    except Exception as e:
        print(f"✓ Erreur attendue pour triangulation inexistante: {e}")


def main():
    """Point d'entrée principal."""
    print("Client de test pour les APIs")
    print("Assurez-vous que les serveurs sont démarrés:")
    print("- PointSetManager sur le port 5000")
    print("- Triangulator sur le port 5001")
    print()
    
    try:
        test_workflow()
        test_error_cases()
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter aux serveurs")
        print("Démarrez les serveurs avec:")
        print("  python start_servers.py manager")
        print("  python start_servers.py triangulator")


if __name__ == "__main__":
    main()