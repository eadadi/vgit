#!/bin/bash
pip install typer[all] pyyaml GitPython
mkdir ~/vgit
chmod +x vgit_cli.py
export vg=`pwd`/vgit_cli.py
echo "write \$vg to use the script"
