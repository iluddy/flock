from setuptools import setup

setup(
    name='flock',
    version='1.0',
    long_description=__doc__,
    packages=['flock'],
    url='ianluddy@gmail.com',
    author_email='ianluddy@gmail.com',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask==0.10.1",
        "blinker==1.3",
        "flask_autodoc",
        "flask_pymongo",
        "tornado",
        "flask_mongoengine",
        "requests",
        "premailer",
        "fabric",
        "lxml",
        "rollbar==0.11.4",
        "celery",
        "redis",
    ],
    entry_points={
        'console_scripts': [
            'flock = flock:app',
        ]
    }
)