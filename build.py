from fabric.api import *

env.host_string = 'ubuntu@ec2-52-30-178-175.eu-west-1.compute.amazonaws.com'
env.key_filename = ['/Users/ianluddy/Dropbox/Code/AWS/flock-ubuntu.pem']

app_dir = '/data/www/flock'
virtualenv = '/data/www/env'

def build_production():
    with cd(app_dir):
        sudo('git pull')
        sudo('source {}/bin/activate'.format(virtualenv))
        sudo('python {}/setup.py install'.format(app_dir))
        sudo('service flock restart', pty=False)

if __name__ == '__main__':
    build_production()