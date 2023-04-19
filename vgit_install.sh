#!/bin/bash
pip install typer[all] pyyaml GitPython
pip install pyinstaller
echo "Invoking pyinstaller vgit_cli.py..."
pyinstaller vgit_cli.py -n vg
echo "add ./dist/vg/vg to your PATH, for example:\n\tln -s \`pwd\`/dist/vg/vg /bin/vg"
