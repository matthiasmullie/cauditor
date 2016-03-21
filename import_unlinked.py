#!/usr/bin/env python3

import sys
import os

# add path where packages are located in ElasticBeanstalk
sys.path.append('/opt/python/run/venv/lib/python3.4/site-packages/')
sys.path.append('/opt/python/run/venv/lib64/python3.4/site-packages/')

# add current directory to ensure these modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from cauditor import jobs
from cauditor import models
from cauditor.container import Container

container = Container(os.environ)
model = models.projects.Model(container.mysql)
projects = model.select(github_hook=None)
for project in projects:
    # import all missing commits
    jobs.execute(container, 'php-rest', {
        'slug': project['name'],
        'git': project['git'],
        'all': True,
    }, 0)
