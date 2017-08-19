activate_this = 'D:/sprintbiz/venv/Scripts/activate_this.py'
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site
from django.core.wsgi import get_wsgi_application

site.addsitedir('D:\sprintbiz\venv\Lib\site-packages')

sys.path.append('C:\Users\sawukpaw\Documents\Acard\sos\sprintbiz')
sys.path.append('C:\Users\sawukpaw\Documents\Acard\sos')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sprintbiz.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sprintbiz.settings")

application = get_wsgi_application()
