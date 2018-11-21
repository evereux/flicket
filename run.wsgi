activate_this = r'C:\python\flicket\env\Scripts\activate_this.py'

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys, os
# application environment so apache can load application.
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

from application import app as application
