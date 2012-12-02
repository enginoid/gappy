from distutils.core import setup
from commands import CheckCommand

setup(
    name='gappy',
    version='0.0.1',
    author='Fred Jonsson',
    author_email='fred@pyth.net',
    packages=['gappy'],
    cmdclass={'codecheck': CheckCommand},
    scripts=[],
    url='https://github.com/enginous/gappy',
)
