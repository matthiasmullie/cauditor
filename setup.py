try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="cauditor",
    description="Figure out complexity hotspots in the blink of an eye.",
    url="http://www.cauditor.org",
    author="Matthias Mullie",
    author_email="cauditor@mullie.eu",
    version="0.1",
    install_requires=["nose"],
    packages=["cauditor"],
    scripts=[],
)
