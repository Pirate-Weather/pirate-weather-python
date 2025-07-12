import os

from setuptools import find_packages, setup

__version__ = "0.0.10"


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")) as f:
    README = f.read()

repo_url = "https://github.com/Pirate-Weather/pirate-weather-python"
setup(
    version=__version__,
    name="pirateweather",
    packages=find_packages(),
    install_requires=["requests==2.32.4", "pytz==2025.2", "aiohttp==3.12.13"],
    description="The Pirate Weather API wrapper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Pirate-Weather",
    url=repo_url,
    download_url=f"{repo_url}/archive/{__version__}.tar.gz",
    license="GPLv3 License",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
