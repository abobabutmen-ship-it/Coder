# Documentation for versions manifest and usage

VERSION MANIFEST
----------------

Path: versions/manifest.json

Structure: JSON array of version objects. Each version object contains:
- version: semver string
- date: ISO date
- changelog: short description
- characteristics: dict with arbitrary keys (supported_langs, features, size, breaking_changes)
- assets: list of assets
  - name: string
  - path: path within repository to asset file
  - checksum: optional (sha256 hex)
  - size: approximate size in bytes
  - platform: e.g., source, linux, windows

CLI
---

Commands (core/versions_cli.py):
- coder-cli versions list
- coder-cli versions show <version>
- coder-cli versions download <version> <asset> [--out <path>]

API
---

- GET /versions -> list
- GET /versions/{version} -> version details
- GET /versions/{version}/assets/{asset_name}/download -> download file

How to add artifacts
--------------------
1. Place small artifact files under versions/artifacts/, name them clearly (e.g. coder-0.1.1-source.zip)
2. Update versions/manifest.json with the new version entry and asset path
3. Commit and push

CI (optional)
-------------
You can add a workflow to build artifacts and commit them to the repo or create a release. Using GitHub Releases is recommended for larger artifacts.
