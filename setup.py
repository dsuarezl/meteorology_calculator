from setuptools import setup, find_packages


# Debugging: Print found packages
found_packages = find_packages(where='src')
print("Found packages:", found_packages)

setup(
    name='meteorology_calculator',
    version='0.1',
    package_dir={'': 'src'},
    packages=found_packages
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
    ],
    description='Module for meteorology calculations',
    author='Daniel',
    author_email='dsuarezl@ull.edu.es',
)