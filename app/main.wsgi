# /usr/bin/python

import os
import sys
sys.path.insert(0, '/home/pi/Python/raspAPI/app')
os.system('python --version')
print(sys.path)

sys.stdout = sys.stderr


from main import app as application

