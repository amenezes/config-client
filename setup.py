from config import __version__

from collections import OrderedDict

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="config-client",
    version=f"{__version__}",
    author="alexandre menezes",
    author_email="alexandre.fmenezes@gmail.com",
    description="config service client for Spring Cloud Config Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://github.com/amenezes/config-client",
    packages=setuptools.find_packages(),
    python_requires=">=3.6.0",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://github.com/amenezes/config-client"),
            ("Code", "https://github.com/amenezes/config-client"),
            ("Issue tracker", "https://github.com/amenezes/config-client/issues"),
        )
    ),
    install_requires=["attrs>=19.1.0", "glom>=19.2.0", "requests>=2.22.0"],
    tests_require=[
        "pytest",
        "flake8",
        "flake8-blind-except",
        "flake8-polyfill",
        "pytest-cov",
        "pytest-mock",
        "isort",
        "black",
        "mypy",
    ],
    extras_require={"cli": ["cleo>=0.7.6"]},
    setup_requires=["setuptools>=38.6.0"],
    entry_points={"console_scripts": ["config=config.__main__:application.run [cli]"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: AsyncIO",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Java Libraries",
    ],
)
