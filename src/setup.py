
from setuptools import setup, find_packages

setup(
    name='markov_genetic_project',
    version='1.0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'networkx',
        'matplotlib',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'run-project=main:main',
        ],
    },
    author='Nikita Lolenko',
    author_email='nik@loleenko.ru',
    description='Проект по анализу цепей Маркова и генетических алгоритмов',
)