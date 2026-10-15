"""Installer for the collective.contact.facetednav package."""

from setuptools import find_packages
from setuptools import setup

long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n"
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.rst").read()
    + "\n"
)


setup(
    name="collective.contact.facetednav",
    version="2.0.0.dev0",
    description="Faceted navigation view for collective.contact.core directory",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
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
        "plone.app.layout",
        "plone.behavior",
        "plone.theme",
        "Products.CMFCore",
        "Products.GenericSetup",
        "Products.statusmessages",
        "Zope",
    ],
    extras_require={
        "test": [
            "ecreall.helpers.testing",
            "plone.app.robotframework",
            "plone.app.testing",
            "plone.browserlayer",
            "plone.registry",
            "plone.testing",
            "Products.CMFPlone",
            "robotsuite",
        ],
    },
    entry_points="""
    """,
)
