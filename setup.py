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
        "flask",
        "blinker",
        "flask_autodoc",
        "flask_pymongo",
        "tornado",
        "flask_mongoengine",
        "requests",
        "premailer",
        "lxml"
    ],
    entry_points={
        'console_scripts': [
            'flock = flock:run',
        ]
    }
)