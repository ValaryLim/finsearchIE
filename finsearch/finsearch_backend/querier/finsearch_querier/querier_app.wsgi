import logging
import sys
print(sys.executable)
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/finsearch_querier')
from querier_app import app as application
application.secretkey = 'finsearch'