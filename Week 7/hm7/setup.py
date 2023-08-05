from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder_bohdanbb',
    version='0.0.1',
    description='This script sorts your folder',
    url='http://github.com/dummy_user/useful',
    author='Flying Circus',
    author_email='flyingcircus@example.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['markdown'],
    entry_points={'console_scripts': [
        'sort = clean_folder.sort:main']}
)
