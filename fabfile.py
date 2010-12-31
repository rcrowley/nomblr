from fabric.api import *
from fabric.contrib.project import rsync_project

env.hosts = ['nomblr.com']
env.key_filename = '/home/vagrant/.ssh/id_rsa'
env.user = 'root'

def test():
    run('hostname --fqdn')
    run('whoami')

def blueprint():
    local('blueprint show nomblr -P')
    rsync_project(local_dir='nomblr', remote_dir='/etc/puppet/modules')
    local('rm -rf nomblr')
    #puppet()

def deploy():
    run('mkdir -p /usr/local/share/wsgi')
    local('git archive --format=tar --prefix=nomblr/ HEAD | gzip >nomblr.tar.gz')
    put('nomblr.tar.gz', '/tmp/')
    with cd('/usr/local/share/wsgi'):
        run('tar xf /tmp/nomblr.tar.gz')
    with settings(warn_only=True):
        result = run('kill -HUP $(cat /var/run/nomblr.pid)')
    if result.failed:
        run('start nomblr')

def puppet():
    run('puppet apply --verbose /etc/puppet/manifests/site.pp')
