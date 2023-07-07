from setuptools import find_packages, setup

setup(
    name='artisan_tools',
    packages=find_packages(),
    version='3.0.0',
    description='Artisan tools library',
    install_requires=['mysql-connector', 'requests', 'psutil' ],
    author='Darrion Whitfield',
    license='MIT',
)

# ro build python setup.py bdist_wheel