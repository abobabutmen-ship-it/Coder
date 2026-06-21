# versions CLI
import os
import click
import json
from core.versions import list_versions, get_version, download_asset

@click.group()
def versions_cli():
    """Version management commands"""
    pass

@versions_cli.command('list')
def versions_list():
    vs = list_versions()
    for v in vs:
        print(f"{v.get('version')} - {v.get('date')} - {v.get('changelog')}")

@versions_cli.command('show')
@click.argument('version')
def versions_show(version):
    v = get_version(version)
    if not v:
        print('not found')
        return
    print(json.dumps(v, indent=2, ensure_ascii=False))

@versions_cli.command('download')
@click.argument('version')
@click.argument('asset')
@click.option('--out', '-o', default=None, help='Output path')
def versions_download(version, asset, out):
    if out is None:
        out = os.path.join(os.getcwd(), asset)
    try:
        meta = download_asset(version, asset, out)
        print('Downloaded to', meta['path'])
        print('checksum', meta['checksum'])
    except Exception as e:
        print('error:', e)
