#!/home/vlim/anaconda3/bin/python
import logging
import sys
print(sys.executable)
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/finsearch_backend_query')
from backend_app import app as application
application.secretkey = 'finsearch'
