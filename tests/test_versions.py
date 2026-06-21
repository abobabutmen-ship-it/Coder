from core.versions import list_versions, get_version


def test_manifest_loads():
    vs = list_versions()
    assert isinstance(vs, list)
    assert any(v.get('version') == '0.1.0' for v in vs)


def test_get_version_found():
    v = get_version('0.1.0')
    assert v is not None
    assert v.get('version') == '0.1.0'
