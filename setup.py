from distutils.core import setup
from setuptools import find_packages

setup(
    name='wallex',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    version='0.4.1',
    license='MIT',
    description='Wallex cryptocurrency exchange python sdk',
    author='amiwrpremium',
    author_email='amiwrpremium@gmail.com',
    url='https://github.com/amiwrpremium/wallex',
    keywords=['wallex', 'crypto', 'exchange', 'API', "SDK"],
    install_requires=[
        'requests',
        'simplejson',
        'deprecation',
        'python-socketio==4.6.1',
        'python-engineio==3.14.2',
        'websocket-client==1.3.2',
        'aiohttp[speedups]',
        'pydantic'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
