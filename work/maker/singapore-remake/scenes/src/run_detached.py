"""Runs a command in the background, logs to logs/<name>.log. Usage: run_detached.py <name> <cwd> <cmd...>"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
name, cwd, cmd = sys.argv[1], sys.argv[2], sys.argv[3:]
log = open(ROOT / 'logs' / (name + '.log'), 'wb')
p = subprocess.Popen(['cmd', '/c', *cmd], cwd=cwd, stdout=log, stderr=subprocess.STDOUT,
                     creationflags=0x00000008 | 0x00000200)
print('started', name, p.pid)
