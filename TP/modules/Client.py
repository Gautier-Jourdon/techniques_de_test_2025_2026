import requests
from TP.modules.PointSet import PointSet
from TP.modules.Triangulation import Triangulation

class ClientAPI:
    def __init__(self, url_manager="http://127.0.0.1:5000", url_triangulator="http://127.0.0.1:5001"):
        self.url_manager = url_manager.rstrip('/')
        self.url_triangulator = url_triangulator.rstrip('/')
    
    def enregistrer_ensemble(self, ensemble: PointSet) -> str:
        donnees = ensemble.vers_octets()
        
        reponse = requests.post(
            f"{self.url_manager}/pointset",
            data=donnees,
            headers={"Content-Type": "application/octet-stream"}
        )
        
        if reponse.status_code == 201:
            resultat = reponse.json()
            return resultat["pointSetId"]
        else:
            self._gerer_erreur(reponse, "Erreur lors de l'enregistrement")
    
    def recuperer_ensemble(self, id_ensemble: str) -> PointSet:
        reponse = requests.get(f"{self.url_manager}/pointset/{id_ensemble}")
        
        if reponse.status_code == 200:
            return PointSet.depuis_octets(reponse.content)
        else:
            self._gerer_erreur(reponse, "Erreur lors de la récupération de l'ensemble")
    
    def recuperer_triangulation(self, id_ensemble: str) -> Triangulation:
        reponse = requests.get(f"{self.url_triangulator}/triangulation/{id_ensemble}")
        
        if reponse.status_code == 200:
            return Triangulation.depuis_octets(reponse.content)
        else:
            self._gerer_erreur(reponse, "Erreur lors de la récupération de la triangulation")

    def _gerer_erreur(self, reponse, contexte):
        message = f"HTTP {reponse.status_code}"
        try:
            donnees = reponse.json()
            message += f": {donnees.get('message', 'Erreur inconnue')}"
        except:
            message += f": {reponse.text}"
        raise Exception(f"{contexte}: {message}")
