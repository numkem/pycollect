from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('./requirements.txt')

reqs = [str(ir.req for ir in install_reqs)]

setup(
    name='pycollect',
    version='0.1',
    packages=['lib', 'plugins'],
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    scripts=['pycollect.py']
)
