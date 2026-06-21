# Integrate metrics CLI into main CLI
from core.cli import cli
from core.cli_metrics import metrics_cli

cli.add_command(metrics_cli, name='metrics')
