from distutils.core import setup

setup(
    name='CatchTheLionRemade',
    version='1.0',
    packages=['AlphaBeta', 'Game', 'GUI', 'MonteCarlo'],
    package_dir={'': '.'},
    url='https://github.com/bruno-sfr/CatchTheLionRemade/tree/main',
    license='',
    author='brunoschaffer',
    author_email='brunoschaffer24@gmail.com',
    description='',
    install_requires=[
        'Pillow>=9.0.0',    # Requires Pillow (PIL) version 9.0.0 or newer
        'matplotlib>=3.0',  # Requires Matplotlib version 3.0 or newer
    ]
)
