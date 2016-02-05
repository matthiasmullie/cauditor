try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'cauditor',
    'description': 'Figure out complexity hotspots in the blink of an eye.',
    'url': 'http://www.cauditor.org',
    'download_url': 'http://www.github.com/matthiasmullie/cauditor',
    'author': 'Matthias Mullie',
    'author_email': 'cauditor@mullie.eu',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['analyzers', 'controllers', 'importers', 'listeners', 'models'],
    'scripts': [],
}

setup(**config)
