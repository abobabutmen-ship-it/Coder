import json
import os
import hashlib
from typing import List, Optional, Dict

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), '..', 'versions', 'manifest.json')


def _load_manifest() -> List[dict]:
    path = os.path.abspath(MANIFEST_PATH)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def list_versions() -> List[dict]:
    return _load_manifest()


def get_version(version: str) -> Optional[dict]:
    for v in _load_manifest():
        if v.get('version') == version:
            return v
    return None


def _checksum_for_file(path: str, algo: str = 'sha256') -> str:
    h = hashlib.new(algo)
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def download_asset(version: str, asset_name: str, out_path: str) -> Dict[str, str]:
    """Copy asset stored in repo (versions/artifacts/) to out_path and return metadata.

    Returns: { 'path': out_path, 'checksum': str }
    """
    v = get_version(version)
    if not v:
        raise FileNotFoundError(f"version {version} not found")
    for a in v.get('assets', []):
        if a.get('name') == asset_name:
            asset_path = os.path.join(os.path.dirname(__file__), '..', a.get('path'))
            asset_path = os.path.abspath(asset_path)
            if not os.path.exists(asset_path):
                raise FileNotFoundError(f"asset file not found: {asset_path}")
            # copy
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(asset_path, 'rb') as src, open(out_path, 'wb') as dst:
                for chunk in iter(lambda: src.read(8192), b''):
                    dst.write(chunk)
            checksum = _checksum_for_file(asset_path)
            return {'path': out_path, 'checksum': checksum}
    raise FileNotFoundError(f"asset {asset_name} not found in version {version}")
