# -*- coding: utf-8 -*-
"""Installer for the collective.contact.facetednav package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n" + "\n" + open("CONTRIBUTORS.rst").read() + "\n" + open("CHANGES.rst").read() + "\n"
)


setup(
    name="collective.contact.facetednav",
    version="2.0.0.dev0",
    description="Faceted navigation view for collective.contact.core directory",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="contact,dexterity,faceted,search",
    author="Cédric Messiant",
    author_email="cedricmessiant@ecreall.com",
    url="http://pypi.python.org/pypi/collective.contact.facetednav",
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "collective.contact.core",
        "eea.facetednavigation",
        "plone.api",
        "Products.CMFPlone",
        "setuptools",
    ],
    extras_require={
        "test": [
            "ecreall.helpers.testing",
            "plone.app.robotframework",
            "plone.app.testing",
        ],
    },
    entry_points="""
    """,
)
