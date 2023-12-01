
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.1'
setup(name='pymddoc',
    version='{}'.format(version),
    description='Interface for programmatically generating markdown documents with code snippets.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/devincornell/pymddoc',
    author='Devin J. Cornell',
    author_email='devin@devinjcornell.com',
    license='MIT',
    packages=find_packages(include=['pymddoc', 'pymddoc.*']),
    install_requires=['setuptools', 'jinja2', 'pypandoc'],
    zip_safe=False,
    download_url='https://github.com/devincornell/pymddoc/archive/v{}.tar.gz'.format(version)
)


