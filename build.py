from fabric.api import *
from time import sleep

env.host_string = 'ubuntu@ec2-52-30-178-175.eu-west-1.compute.amazonaws.com'
env.key_filename = ['/Users/ianluddy/Dropbox/Code/AWS/flock-ubuntu.pem']

app_dir = '/home/flock/flock'
virtualenv = '/home/flock/env'

def build_production():
    with cd(app_dir):
        sudo('git stash')
        sudo('git pull')
        sudo('source {}/bin/activate && python {}/setup.py install'.format(virtualenv, app_dir))
        sudo('monit restart all', pty=False)
        sudo('git stash pop')


if __name__ == '__main__':
    build_production()