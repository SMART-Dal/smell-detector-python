from setuptools import setup, find_packages

setup(
    name='PySmellDetector',
    version='1.0.0',
    author='Harsh Vaghani',
    author_email='harshvaghani00@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pytest~=7.4.3',
        'networkx~=3.2.1',
        'astunparse~=1.6.3',
        'pytest_mock==3.12.0',
        'typer~=0.9.0'
    ],
    entry_points={
        'console_scripts': [
            'py-smell-detector=src.cli:app'
        ]
    },
    include_package_data=True,
    package_data={'smells': ['default_config.json']},
)
