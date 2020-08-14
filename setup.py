import runpy
from setuptools import setup, find_packages

PACKAGE_NAME = "chainlink-tools"
version_meta = runpy.run_path("./chainlink_tools/__version__.py")
VERSION = version_meta["__version__"]
URL = version_meta["__url__"]


with open("README.md", "r") as fh:
    long_description = fh.read()


def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        packages=find_packages(),
        install_requires=parse_requirements("requirements.txt"),
        scripts=["bin/chainlink-tools"],
        include_package_data=True,
        description="Utilities for operating a chainlink node.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        keywords="chainlink oracle smart contract",
        author="dursk",
        license="MIT",
        project_urls={"Source": URL,},
    )
