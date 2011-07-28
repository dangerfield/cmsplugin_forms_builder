
from setuptools import setup, find_packages
 
 
setup(
    name = "cmsplugin-forms-builder",
    version = __import__("cmsplugin_forms_builder").__version__,
    author = "William Dangerfield",
    author_email = "dangerfield@gmail.com",
    description = ("A CMS plugin for django-forms-builder"),
    long_description = open("README.rst").read(),
    url = "https://github.com/dangerfield/cmsplugin_forms_builder",
    zip_safe = False,
    include_package_data = True,
    packages = find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ]
)

