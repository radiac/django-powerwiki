import os

from setuptools import find_packages, setup

from powerwiki import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django-powerwiki",
    version=__version__,
    author="Richard Terry",
    author_email="code@radiac.net",
    description=("A wiki system for Django"),
    license="BSD",
    url="http://radiac.net/projects/django-powerwiki/",
    long_description=read("README.rst"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=True,
    install_requires=[
        "Django>=2.2",
        "django-yaa-settings",
        "beautifulsoup4",
        "docutils",
    ],
    packages=find_packages(),
    include_package_data=True,
)
