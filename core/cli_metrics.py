import click
import json
from core.metrics import analyze_code_metrics
from core.security_scan import scan_python_with_bandit
from core.cli import _read_code

@click.group()
def metrics_cli():
    """Metrics and security scan commands"""
    pass

@metrics_cli.command('metrics')
@click.option('--lang', required=True, type=click.Choice(['py','js','cpp']))
@click.option('--file', '-f', type=click.Path(exists=True), help='Path to file')
@click.option('--code', '-c', help='Raw code string')
def cmd_metrics(lang, file, code):
    src = _read_code(file, code)
    res = analyze_code_metrics(lang, src)
    click.echo(json.dumps(res, ensure_ascii=False, indent=2))

@metrics_cli.command('scan')
@click.option('--file', '-f', type=click.Path(exists=True), help='Path to file')
@click.option('--code', '-c', help='Raw code string')
def cmd_scan(file, code):
    src = _read_code(file, code)
    res = scan_python_with_bandit(src)
    click.echo(json.dumps(res, ensure_ascii=False, indent=2))
