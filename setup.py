from setuptools import setup, find_packages

version = '0.1'

setup(
    name='Selendis',
    version=version,
    description='Tornado-based websocket MUD',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

