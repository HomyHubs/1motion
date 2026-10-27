"""Compare MANIFEST.sha256 rows with git show HEAD:<file>. Run after the commit finished."""
import hashlib
import subprocess

PKG = 'make-editorial-explainer'
n = bad = 0
for line in open(PKG + '/MANIFEST.sha256', encoding='utf-8'):
    digest, name = line.rstrip('\n').split('  ', 1)
    data = subprocess.run(['git', 'show', 'HEAD:' + PKG + '/' + name], capture_output=True).stdout
    n += 1
    if hashlib.sha256(data).hexdigest() != digest:
        bad += 1
        print('MISMATCH', name)
print('rows', n, 'mismatch', bad)
