from setuptools import setup, find_packages

setup(
    name='shared',
    version='0.1.0',
    packages=find_packages(),
    py_modules=['exceptions', 'constants', 'response', 'http_client', 'logger', 'error_handlers'], 
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    author='huydq2k1',
    description='Shared internal package for microservices'
)
