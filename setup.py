from setuptools import setup, find_packages

setup(
    name='meteorology_calculator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
    ],
    description='Module for meteorology calculations',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    author='Daniel',
    author_email='dsuarezl@ull.edu.es',
    # url='http://example.com/meteorology_calculator',  # Optional
)