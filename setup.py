try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'caudit',
    'description': 'Figure out complexity hotspots in the blink of an eye.',
    'url': 'http://www.caudit.org',
    'download_url': 'http://www.github.com/matthiasmullie/caudit.org',
    'author': 'Matthias Mullie',
    'author_email': 'caudit@mullie.eu',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['analyzers', 'controllers', 'importers', 'listeners', 'models'],
    'scripts': [],
}

setup(**config)
