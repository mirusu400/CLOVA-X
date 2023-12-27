import re
from setuptools import setup, find_packages


def get_version():
    filename = "clovax/__init__.py"
    with open(filename) as f:
        match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M)
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="clovax",
    version=get_version(),
    description="Unofficial CLOVA X API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="mirusu400",
    author_email="mirusu400@naver.com",
    url="https://github.com/mirusu400/CLOVA-X-API",
    install_requires=["requests"],
    packages=find_packages(exclude=[]),
    keywords=["ClovaX", "Naver", "CLOVA", "CLOVA X", "CLOVA X API"],
    python_requires=">=3.7",
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
