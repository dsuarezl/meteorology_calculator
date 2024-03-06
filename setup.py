from setuptools import setup, find_packages

setup(
    name='meteorology_calculator',
    version='0.1',
    package_dir={'': 'src'},  # Tells setuptools that packages are under src
    packages=find_packages(where='src'),  # Finds packages in src
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
    ],
    description='Module for meteorology calculations',
    author='Daniel',
    author_email='dsuarezl@ull.edu.es',
)