# Techniques de test 2025/2026

Forkez le repository pour pouvoir en faire votre version avec votre travail.  
Le sujet du TP se trouve [ici](./TP/SUJET.md)

## Étudiant  

Nom : Jourdon  
Prénom : Gautier  
Groupe de TP : Gr1 (e.g. M1 ILSEN classique - changement en Groupe IA)  

## Remarques particulières

Etant en cours de basculement en filière IA, 
lors des prochains TPs je serai présent dans 
le groupe des IAs.

---

# Implémentation du Micro-service de Triangulation

## Description

Ce projet implémente un micro-service de triangulation composé de plusieurs modules :

- **PointSetManager** : API HTTP pour la gestion des ensembles de points
- **Triangulator** : API HTTP pour le calcul de triangulation de Delaunay
- **Point, PointSet, PointSetId** : Classes de base pour la manipulation des données
- **triangulation** : Algorithmes de triangulation et structures de données

## Structure du projet

```
├── Point.py              # Classe Point (coordonnées 2D)
├── PointSet.py           # Classe PointSet (ensemble de points + sérialisation binaire)
├── PointSetId.py         # Classe PointSetId (identifiants UUID)
├── PointSetManager.py    # API PointSetManager (Flask)
├── triangulation.py      # Triangulation de Delaunay + API Triangulator
├── whichForm.py          # Utilitaires pour déterminer les formes
├── requirements.txt      # Dépendances de production
├── dev_requirements.txt  # Dépendances de développement
├── start_servers.py      # Script pour démarrer les serveurs
├── client_test.py        # Client de test pour les APIs
├── test_basic.py         # Tests de base des classes
└── demo_apis.py          # Démonstration complète des APIs
```

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Pour le développement :
```bash
pip install -r dev_requirements.txt
```

## Utilisation

### Démarrage des serveurs

Dans des terminaux séparés :

```bash
# Terminal 1 : PointSetManager (port 5000)
python start_servers.py manager

# Terminal 2 : Triangulator (port 5001)  
python start_servers.py triangulator
```

Ou directement :
```bash
# PointSetManager
python PointSetManager.py

# Triangulator
python triangulation.py
```

### Tests et démonstrations

```bash
# Tests de base des classes
python test_basic.py

# Test complet des APIs
python client_test.py

# Démonstration automatique (démarre les serveurs)
python demo_apis.py
```

### Utilisation programmatique

```python
from Point import Point
from PointSet import PointSet
from PointSetId import PointSetId
from triangulation import DelaunayTriangulator

# Créer des points
points = [Point(0.0, 0.0), Point(1.0, 0.0), Point(0.5, 1.0)]
point_set = PointSet(points)

# Triangulation
triangulation = DelaunayTriangulator.triangulate(point_set)
print(f"Triangulation avec {len(triangulation.triangles)} triangles")

# Sérialisation binaire
binary_data = point_set.to_binary()
restored_point_set = PointSet.from_binary(binary_data)
```

## APIs

### PointSetManager (port 5000)

- `POST /pointset` : Enregistrer un nouveau PointSet (format binaire)
- `GET /pointset/{id}` : Récupérer un PointSet par son UUID

### Triangulator (port 5001)

- `GET /triangulation/{id}` : Calculer la triangulation d'un PointSet

## Format binaire

### PointSet
- 4 bytes : nombre de points (unsigned long)
- Pour chaque point : 8 bytes (4 bytes X + 4 bytes Y, float)

### Triangles
- Partie 1 : PointSet (sommets)
- Partie 2 : Triangles
  - 4 bytes : nombre de triangles
  - Pour chaque triangle : 12 bytes (3 × 4 bytes, indices des sommets)

## Architecture

```
Client
  ↓
PointSetManager ←→ Database (mémoire)
  ↓
Triangulator
```

Le workflow typique :
1. Client envoie PointSet → PointSetManager
2. PointSetManager retourne PointSetID
3. Client demande triangulation → Triangulator avec PointSetID
4. Triangulator récupère PointSet → PointSetManager  
5. Triangulator calcule et retourne triangulation

## Développement

### Tests
```bash
make test          # Tous les tests
make unit_test     # Tests unitaires seulement
make perf_test     # Tests de performance seulement
```

### Qualité du code
```bash
make lint          # Vérification avec ruff
make coverage      # Rapport de couverture
make doc           # Génération documentation
```

## Fonctionnalités implémentées

✅ **Classes de base**
- Point : coordonnées 2D avec getters/setters
- PointSetId : identifiants UUID avec validation
- PointSet : gestion d'ensembles de points + sérialisation binaire

✅ **PointSetManager**
- API HTTP conforme OpenAPI
- Stockage en mémoire
- Validation des données binaires
- Gestion d'erreurs complète

✅ **Triangulator**
- API HTTP conforme OpenAPI
- Algorithme de triangulation (simple, non-Delaunay optimal)
- Communication avec PointSetManager
- Format binaire Triangles

✅ **Sérialisation binaire**
- Format PointSet conforme spécification
- Format Triangles conforme spécification
- Validation et gestion d'erreurs

✅ **Infrastructure**
- Scripts de démarrage
- Client de test
- Documentation
- Gestion d'erreurs HTTP appropriée

## Notes sur l'implémentation

- L'algorithme de triangulation implémenté est fonctionnel mais simple
- Pour une vraie triangulation de Delaunay, il faudrait implémenter l'algorithme de Bowyer-Watson
- Le stockage est en mémoire (pas de vraie base de données)
- Les APIs sont conformes aux spécifications OpenAPI fournies
