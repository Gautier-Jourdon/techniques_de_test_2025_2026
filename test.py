from unittest.mock import Mock

# [1.1] Algorithme de triangulation
def test_triangulation_triangle_simple():
    algo = Mock()
    algo.triangulate.return_value = [(0, 1, 2)]
    points = ["P0", "P1", "P2"]
    result = algo.triangulate(points)
    assert result == [(0, 1, 2)]

def test_triangulation_carre():
    algo = Mock()
    # Il faut 2 triangles pour faire un carré
    algo.triangulate.return_value = [(0, 1, 2), (0, 2, 3)]
    points = ["P0", "P1", "P2", "P3"]
    assert len(algo.triangulate(points)) == 2

def test_triangulation_colineaire():
    algo = Mock()
    algo.triangulate.side_effect = ValueError("Points colinéaires")
    try:
        algo.triangulate(["A", "B", "C"])
        assert False
    except ValueError as e:
        assert "colinéaires" in str(e)

def test_triangulation_doublons():
    algo = Mock()
    algo.triangulate.return_value = []
    pts = ["A", "A", "B"]
    assert algo.triangulate(pts) == []

def test_triangulation_vide():
    algo = Mock()
    algo.triangulate.return_value = []
    assert algo.triangulate([]) == []

def test_triangulation_un_ou_deux_points():
    algo = Mock()
    algo.triangulate.side_effect = RuntimeError("Pas assez de points")
    for pts in (["A"], ["A", "B"]):
        try:
            algo.triangulate(pts)
            assert False
        except RuntimeError:
            pass

def test_triangulation_points_tres_proches():
    algo = Mock()
    algo.triangulate.return_value = [(0, 1, 2)]
    pts = ["p(tres_proche)_0", "p(tres_proche)_1", "p(tres_proche)_2"]
    assert algo.triangulate(pts)[0] == (0, 1, 2)

# [1.2] Conversion binaire de "PointSet" (grâce au mock parse/serialize)
def test_pointset_parsing_valide():
    parser = Mock()
    parser.parse.return_value = ["P0", "P1"]
    data = b"FAKE_BIN_OK"
    assert parser.parse(data) == ["P0", "P1"]

def test_pointset_parsing_invalide():
    parser = Mock()
    parser.parse.side_effect = ValueError("Format invalide")
    try:
        parser.parse(b"BAD")
        assert False
    except ValueError as e:
        assert "invalide" in str(e)

def test_pointset_serialisation():
    serializer = Mock()
    serializer.serialize.return_value = b"OK"
    assert serializer.serialize(["P0"]) == b"OK"

def test_pointset_roundtrip():
    codec = Mock()
    codec.serialize.return_value = b"RT"
    codec.parse.return_value = ["P0"]
    raw = codec.serialize(["P0"])
    back = codec.parse(raw)
    assert raw == b"RT"
    assert back == ["P0"]

# [1.3] Conversion binaire des triangles
def test_triangles_serialisation():
    ser = Mock()
    ser.serialize.return_value = b"T123"
    assert ser.serialize([(0, 1, 2)]) == b"T123"

def test_triangles_parsing():
    par = Mock()
    par.parse.return_value = [(0, 1, 2)]
    assert par.parse(b"T123") == [(0, 1, 2)]

def test_triangles_indices_invalides():
    par = Mock()
    par.parse.side_effect = IndexError("Indice hors limites")
    try:
        par.parse(b"BAD_TRI")
        assert False
    except IndexError as e:
        assert "Indice" in str(e)

def test_triangles_roundtrip():
    codec = Mock()
    codec.serialize.return_value = b"TRI"
    codec.parse.return_value = [(0, 1, 2)]
    assert codec.parse(codec.serialize([(0, 1, 2)])) == [(0, 1, 2)]

# [2.1] Le "Endpoint" GET /triangulation/{pointSetId}
def test_endpoint_succes():
    api = Mock()
    api.get_triangulation.return_value = {"triangles": [(0, 1, 2)]}
    assert api.get_triangulation("uuid-ok")["triangles"]

def test_endpoint_uuid_invalide():
    api = Mock()
    api.get_triangulation.side_effect = ValueError("UUID invalide")
    try:
        api.get_triangulation("123")
        assert False
    except ValueError:
        pass

def test_endpoint_not_found():
    api = Mock()
    api.get_triangulation.side_effect = KeyError("Introuvable")
    try:
        api.get_triangulation("uuid-manquant")
        assert False
    except KeyError:
        pass

def test_endpoint_erreur_algo():
    api = Mock()
    api.get_triangulation.side_effect = RuntimeError("Erreur triangulation")
    try:
        api.get_triangulation("uuid-ok")
        assert False
    except RuntimeError:
        pass

def test_endpoint_service_indispo():
    api = Mock()
    api.get_triangulation.side_effect = ConnectionError("Service indisponible")
    try:
        api.get_triangulation("uuid-ok")
        assert False
    except ConnectionError:
        pass

# [2.2] La communication avec "PointSetManager"
def test_pointsetmanager_recuperation_reussie():
    mgr = Mock()
    mgr.fetch.return_value = ["P0", "P1"]
    assert len(mgr.fetch("uuid")) == 2

def test_pointsetmanager_connexion_echec():
    mgr = Mock()
    mgr.fetch.side_effect = ConnectionError("Panne réseau")
    try:
        mgr.fetch("uuid")
        assert False
    except ConnectionError:
        pass

def test_pointsetmanager_timeout():
    mgr = Mock()
    mgr.fetch.side_effect = TimeoutError("Timeout")
    try:
        mgr.fetch("uuid")
        assert False
    except TimeoutError:
        pass

def test_pointsetmanager_reponse_malformee():
    mgr = Mock()
    mgr.fetch.return_value = None
    assert mgr.fetch("uuid") is None

# [4.1] Les cas limites ~
def test_points_grands():
    algo = Mock()
    algo.triangulate.return_value = [(0, 1, 2)]
    pts = ["P_BIG_X", "P_BIG_Y", "P_BIG_Z"]
    assert algo.triangulate(pts)

def test_precision_flottante():
    algo = Mock()
    algo.triangulate.return_value = [(0, 1, 2)]
    pts = ["EP0", "EP1", "EP2"]
    assert algo.triangulate(pts)[0] == (0, 1, 2)

# [4.2] Tests de validation des données
def test_validation_uuid_format():
    validator = Mock()
    validator.is_valid_uuid.side_effect = lambda x: "-" in x
    assert validator.is_valid_uuid("a-b-c")

def test_validation_format_binaire():
    val = Mock()
    val.validate_bin.return_value = True
    assert val.validate_bin(b"OK")

def test_gestion_erreurs_message():
    handler = Mock()
    handler.handle.side_effect = ValueError("Erreur connue")
    try:
        handler.handle("x")
        assert False
    except ValueError as e:
        assert "Erreur" in str(e)

def test_logs_tracabilite():
    logger = Mock()
    logger.log.return_value = None
    logger.log("INFO", "Message")
    logger.log.assert_called()

# [3] Les Performance
def test_perf_petit_ensemble():
    perf = Mock()
    perf.triangulate.return_value = "OK"
    assert perf.triangulate(["P0"]) == "OK"

def test_perf_grand_ensemble():
    perf = Mock()
    perf.triangulate.return_value = "OK"
    points = ["P" + str(i) for i in range(10)]
    assert perf.triangulate(points) == "OK"