from fabric.api import *
from time import sleep

env.host_string = 'ubuntu@ec2-52-30-178-175.eu-west-1.compute.amazonaws.com'
env.key_filename = ['/Users/ianluddy/Dropbox/Code/AWS/flock-ubuntu.pem']

app_dir = '/data/www/flock'
virtualenv = '/data/www/env'

def build_production():
    with cd(app_dir):
        sudo('git pull'.format(app_dir))
        sudo('source {}/bin/activate && python {}/setup.py install'.format(virtualenv, app_dir))
        sudo('monit stop flock', pty=False)
        sudo('monit stop celery', pty=False)
        sleep(10)
        sudo('monit start flock', pty=False)
        sudo('monit start celery', pty=False)

if __name__ == '__main__':
    build_production()