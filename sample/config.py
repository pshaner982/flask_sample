

import os
this_dir = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(this_dir, os.pardir))


CSRF_ENABLED = True
SECRET_KEY = 'tiiIsspaassswrdisLTERALLyyUUnunHCAKBLE!!'
FLASK_DEBUG = True

################################################################################
#
#   Database Constants
#
################################################################################
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = f'sqlite:////{os.path.join(BASE_DIR, "sample", "model", "test.db")}'