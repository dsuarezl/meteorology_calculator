from setuptools import setup, find_packages

setup(
    name='meteorology_calculator',
    version='0.1',
    packages=[
        'meteorology_calculator', 
        'meteorology_calculator.anomaly',
        'meteorology_calculator.coldwaves',
        'meteorology_calculator.heatwaves',
        'meteorology_calculator.plotting',
        'meteorology_calculator.z_score'
    ],
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
    ],
    description='Module for meteorology calculations',
    author='Daniel',
    author_email='dsuarezl@ull.edu.es',
)