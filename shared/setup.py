from setuptools import setup, find_packages

setup(
    name='shared',
    version='0.1.0',
    packages=find_packages(where='shared'),
    package_dir={'': 'shared'},
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    author='huydq2k1',
    description='Shared internal package for microservices'
)
