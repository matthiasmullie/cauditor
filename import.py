#!/usr/bin/env python3

import sys
import os
import getopt

# add path where packages are located in ElasticBeanstalk
sys.path.append('/opt/python/run/venv/lib/python3.4/site-packages/')
sys.path.append('/opt/python/run/venv/lib64/python3.4/site-packages/')

# add current directory to ensure these modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from cauditor import jobs
from cauditor import models
from cauditor.container import Container

kwhere = {}
where = []
queue = 'php-rest'
opts, args = getopt.getopt(sys.argv[1:], 't:r:q:', ['type=', 'repo=', 'queue='])
if len(opts) > 0:
    if opts[0][0] in ('-t', '--type') and opts[0][1] == 'unlinked':
        kwhere = {'github_hook': None}
    if opts[0][0] in ('-t', '--type') and opts[0][1] == 'linked':
        where = ['github_hook IS NOT NULL']
    if opts[0][0] in ('-r', '--repo'):
        kwhere = {'name': opts[0][1]}
    if opts[0][0] in ('-q', '--queue'):
        queue = opts[0][1]

container = Container(os.environ)
model = models.projects.Model(container.mysql)
projects = model.select(where=where, **kwhere)
for project in projects:
    # import all missing commits
    jobs.execute(container, queue, {
        'slug': project['name'],
        'git': project['git'],
        'all': True,
    }, 0)
