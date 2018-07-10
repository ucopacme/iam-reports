"""iam-reports setup"""

from iamreports import __version__
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='iam-reports',
    version='0.0.0',
    description='Reporting tools for IAM access in AWS organizational accounts',
    long_description=long_description,
    url='https://github.com/ashleygould/iam-reports',
    author='Ashley Gould',
    author_email='agould@ucop.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='aws organizations iam',
    #packages=find_packages(exclude=['scratch', 'notes']),
    packages=find_packages(),
    install_requires=['boto3', 'docopt', 'PyYAML'],
    package_data={
        'iamreports': [
        ],
    },
    entry_points={
        'console_scripts': [
            'awsorgs=awsorgs.orgs:main',
            'awsaccounts=awsorgs.accounts:main',
            'awsauth=awsorgs.auth:main',
            'awsloginprofile=awsorgs.loginprofile:main',
            'awsorgs-accessrole=awsorgs.accessrole:main',
        ],
    },

)
