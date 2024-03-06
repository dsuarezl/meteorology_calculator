from setuptools import setup, find_packages


# Debugging: Print found packages
found_packages = find_packages(where='src')
print("Found packages:", found_packages)

setup(
    name='meteorology_calculator',
    version='0.1',
    package_dir={'': 'src'},
    packages=[
        'meteorology_calculator',  # El paquete principal
        'meteorology_calculator.anomaly',  # Subpaquete anomaly
        'meteorology_calculator.coldwaves',  # Subpaquete coldwaves
        'meteorology_calculator.heatwaves',  # Subpaquete heatwaves
        'meteorology_calculator.plotting',  # Subpaquete plotting
        'meteorology_calculator.z_score',  # Subpaquete z_score
        # Añade aquí otros subpaquetes según sea necesario
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