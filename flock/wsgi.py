import os, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flock.utils import read_config_file

cfg = read_config_file('/home/flock/flock/configs/flock-production.json')

import __builtin__
__builtin__.flock_cfg = cfg

from flock.app import app

__builtin__.flock_app = app
from flock import views

if __name__ == '__main__':
    app.run()