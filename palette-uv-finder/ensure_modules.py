import sys
import subprocess
import ensurepip

def bootstrap():
    ensurepip.bootstrap()
    pybin = sys.executable
    subprocess.check_call([pybin, '-m', 'pip', 'install', 'Pillow'])
    subprocess.check_call([pybin, '-m', 'pip', 'install', 'imageio'])

