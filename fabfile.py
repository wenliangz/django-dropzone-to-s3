#!/usr/bin/env python

"""
Fabric must be installed to use this script, then simply execute "fab deploy" from the Command Line to
deploy this installation to an AWS EC2 instance.
"""

# Import system modules
import os

# Import third-party modules
from fabric.context_managers import cd
from fabric.operations import sudo, run, put
from fabric.state import env
from fabric.network import ssh


PROJECT_NAME = 'django-dropzone-to-s3'
HOSTNAME = 'myserver.com'
USERNAME = 'ubuntu'
KEY_PATH = '~/.ssh/myserver.pem'
SERVER_PATH = '/home/ubuntu'


def deploy():
    env.user = USERNAME
    env.host_string = HOSTNAME
    env.key_filename = KEY_PATH
    path = SERVER_PATH
    
    with cd(path):
        # Create our project's directory
        run('mkdir ' + PROJECT_NAME, warn_only=True)
    
    with cd(path + '/' + PROJECT_NAME):
        # Ensure dependencies are installed on the server
        sudo('apt-get -y install git apache2 libapache2-mod-wsgi python python-pip')
        
        # Put the files on the server
        put('.', '.')
        sudo('mv site-myserver.conf /etc/apache2/sites-available')
        sudo('a2ensite site-myserver.conf')
        
        # Run the requirements file to ensure all dependencies are met
        sudo('pip install -r reqs.txt')

        # Remove unnecessary files and folders for production
        run('rm -rf .git', warn_only=True)
        run('rm -rf .idea', warn_only=True)
        run('rm .gitignore', warn_only=True)
        run('rm fabfile.py', warn_only=True)
        run('rm README.md', warn_only=True)
        run('find . -name "*.pyc" -exec rm -rf {} \;', warn_only=True)

    # Restart necessary services
    sudo('service apache2 restart')


if __name__ == '__main__':
    print 'Oops, this file is not executable, it\'s meant to be used by Fabric. To execute its functionality, use "fab deploy".'