try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open
import sys

if sys.version_info[:3] < (3, 0, 0):
    sys.stdout.write("Requires Python 3 to run.")
    sys.exit(1)

with open("README.md", encoding="utf-8") as file:
    readme = file.read()

setup(
    name="neuropipe",
    version="1.0.0a1",
    description="Command-line tool for easily scaffolding a machine learning pipeline",
    #long_description=readme,
    #long_description_content_type="text/markdown",
    url="https://github.com/shobrook/neuropipe",
    author="shobrook",
    author_email="shobrookj@gmail.com",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python"
    ],
    keywords="machine learning",
    include_package_data=True,
    packages=["neuropipe"],
    entry_points={"console_scripts": ["neuropipe = neuropipe.neuropipe:main"]},
    install_requires=["pystache"],
    requires=["pystache"],
    python_requires=">=3",
    license="MIT"
)
