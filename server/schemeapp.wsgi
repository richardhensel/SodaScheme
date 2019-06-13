#!/usr/bin/python
print "hello"

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Flask/")

from Scheme import app as application
#application.secret_key = 'kmkjwdv8387495?*&DC'
