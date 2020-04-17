from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    licenses = f.read()

setup(
    name = 'dockensic',
    version = '0.1',
    description = 'Not yet decided',
    url = 'https://github.com/thiru112/docensic',
    license = licenses,
    author = 'Thiru A P',
    author_email = 'thiru.ap112@gmail.com',
    long_description = readme,
    packages = find_packages(exclude=('tests', 'docs')),
    install_requires = [],
    scripts = []
)