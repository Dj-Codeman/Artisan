from setuptools import find_packages, setup

setup(
    name='artisan_tools',
    packages=find_packages(),
    version='1.0.0',
    description='Artisan tools library',
    install_requires=['mysql-connector', 'smtplib' ],
    author='Darrion Whitfield',
    license='MIT',
)