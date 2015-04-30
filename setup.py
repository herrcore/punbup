from setuptools import setup

setup(
    name='punbup',
    version='0.0.1',
    url='https://github.com/herrcore/punbup',
    author='@herrcore, setup @seanmw',
    description='Python unbup script for McAfee .bup files - with some additional fun features. \
     Simple usage will extract all files from a .bup to a directory with the same name as the bup file.',
    install_requires=["olefile"],
    py_modules=['punbup'],
    entry_points={'console_scripts': ['punbup=punbup:main']}
)
