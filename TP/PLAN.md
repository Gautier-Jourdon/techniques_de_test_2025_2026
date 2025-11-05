# Plan de Tests - Le triangulator

## [1] Tests Unitaires - Algorithme de Triangulation

### [1.1] Tests de l'algorithme de triangulation
- **Test avec triangle simple** : Si 3 points formant un triangle valide
- **Test avec carré** : Si 4 points formant un carré alors (2 triangles attendus)
- **Test avec points colinéaires** : Gestion des points alignés
- **Test avec points en double** : Gestion des doublons
- **Test avec ensemble vide** : Si 0 point relié
- **Test avec 1 ou 2 points** : Si c'ets un cas impossibles à trianguler
- **Test avec points très proches** : Pour la précision numérique

### [1.2] Tests de conversion binaire PointSet
- **Test de parsing valide** : Format binaire correct → structure interne valide
- **Test de parsing invalide** : Pour les données tronquées, format incorrect
- **Test de sérialisation** : Structure interne → format binaire
- **Test round-trip** : Parsing puis sérialisation si identique

### [1.3] Tests de conversion binaire Triangles
- **Test de sérialisation triangles** : Transformation de la structure interne au format binaire
- **Test de parsing triangles** : Transformation du format binaire en une structure interne
- **Test d'indices invalides** : Références vers sommets inexistants
- **Test round-trip triangles** : Cohérence des conversions (évidentes en l'occurence)

## [2] Tests d'Intégration - API Triangulator

### [2.1] Endpoint GET /triangulation/{pointSetId}
- **Test 200 - Succès** : PointSet valide → triangulation réussie
- **Test/Erreur 400 - UUID invalide** : Le format d'ID est incorrect (non-UUID) ex: 123456789 au lieu de 123-456-789
- **Test/Erreur 404 - PointSet introuvable** : L'ID est valide mais inexistant
- **Test/Erreur 500 - Erreur triangulation** : Algorithme échoue (points dégénérés)
- **Test/Erreur 503 - Service indisponible** : PointSetManager inaccessible

### [2.2] Communication avec PointSetManager (usage du Mock)
- **Test de récupération réussie** : Mock du PointSetManager retournant données valides
- **Test d'échec de connexion** : Mock simulant une panne réseau
- **Test de timeout** : Mock simulant une réponse lente
- **Test de réponse malformée** : PointSetManager retourne données invalides

## [3] Tests de Performance

### [3.1] Performance de triangulation
(Note : Les nombres de points sont à valeur indicatives, j'ai choisi des valeurs génériques.)
- **Petits ensembles** : 10, 50, 100 points - temps d'exécution
- **Ensembles moyens** : 500, 1000 points - temps d'exécution et mémoire
- **Grands ensembles** : 5000, 10000 points - limites de performance

### [3.2] Performance de conversion binaire
- **Parsing PointSet** : Temps selon taille des données
- **Sérialisation Triangles** : Temps selon nombre de triangles
- **Mémoire utilisée** : Consommation selon taille des structures

## [4] Tests de Qualité et Robustesse

### [4.1] Tests de cas limites
- **Points à l'infini** : Coordonnées très (ou trop) grandes
- **Précision flottante** : Points très proches (epsilon) ~

### [4.2] Tests de validation des données
- **Validation UUID** : Format strict (ou plus strict en tout cas) des identifiants
- **Validation format binaire** : Structures cohérentes
- **Gestion d'erreurs** : Messages d'erreur appropriés
- **Logs et traçabilité** : Informations de debug

## [5] Organisation des Tests

### [5.1] Idée de structure des fichiers
```
tests/
├── unit/
│   ├── test_triangulation_algorithm.py
│   ├── test_binary_pointset.py
│   └── test_binary_triangles.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_pointsetmanager_client.py
├── performance/
│   ├── test_triangulation_perf.py
│   └── test_binary_conversion_perf.py
└── fixtures/
    ├── sample_pointsets/
    └── expected_triangulations/
```

### [5.2] Marqueurs pytest
(Note : Je me suis aidé d'un forum en ligne pour trouver ces derniers)
- **@pytest.mark.unit** : Tests unitaires rapides
- **@pytest.mark.integration** : Tests d'intégration
- **@pytest.mark.performance** : Tests de performance (exclus par défaut)
- **@pytest.mark.slow** : Tests longs à exécuter

### [5.3] Fixtures et mocks
- **Fixtures PointSet** : Jeux de données réutilisables
- **Mock PointSetManager** : Simulation des réponses API
- **Fixtures triangulations** : Résultats attendus pré-calculés

## [6] Couverture et Qualité

### [6.1] Objectifs de couverture
(Note : Pour la couverture, on rappelle qu'elle est différente de la performance)
- **Couverture globale** : ≥ 95% du code
- **Couverture branches** : ≥ 90% des conditions
- **Exclusions** : Configuration, imports, code inaccessible

### [6.2] Outils qualité
- **ruff check** : Respect des règles de style et qualité
- **Documentation** : Docstrings sur toutes les fonctions publiques
- **Type hints** : Annotations de type complètes
        - Est-ce que le point "..." est diponible ?
        - Est-ce que j'ai bien atteint le point "..." ?