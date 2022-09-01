from setuptools import setup

setup(
    name='Tapic',
    version='0.0.1',
    author='Roman Gerlovin',
    author_email='gerroma01@gmail.com',
    description='FastApi app',
    install_requires=[
        'fastapi',
        'uvicorn',
        'SQLAlchemy',
        'pytest',
        'requests',
        'gunicorn'
    ],
    scripts=[
        'app/main.py',
        'scripts/create_db.py'
    ]
)