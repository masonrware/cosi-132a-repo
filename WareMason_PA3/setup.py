from setuptools import setup

setup(
    name = 'WareMason_PA3',
    version = '1.0.0',
    packages = ['WareMason_PA3'],
    install_requires=[
        'Flask',
        'pymongo',
        'nltk'
    ]
)