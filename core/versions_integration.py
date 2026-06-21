# Integrate versions CLI into main CLI group

from core.versions_cli import versions_cli

# after creating main cli group, we add as subcommand
# this file intentionally small; core/cli.py will import and register
