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
    packages=setuptools.find_packages(include=["config", "config.*"]),
    python_requires=">=3.6.0",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://config-client.amenezes.net"),
            ("Code", "https://github.com/amenezes/config-client"),
            ("Issue tracker", "https://github.com/amenezes/config-client/issues"),
        )
    ),
    install_requires=["attrs>=19.1.0", "glom>=19.2.0", "requests>=2.22.0"],
    tests_require=[
        "pytest==5.3.4",
        "flake8==3.7.8",
        "flake8-blind-except==0.1.1",
        "flake8-polyfill==1.0.2",
        "pytest-cov==2.9.0",
        "pytest-mock==3.1.0",
        "isort==4.3.21",
        "black==19.10b0",
        "mypy>=0.770",
        "python-dotenv>=0.13.0",
        "aiohttp>=3.5.4",
        "flask>=1.0.0",
    ],
    extras_require={
        "cli": ["cleo>=0.7.6", "python-dotenv>=0.10.3"],
        "docs": ["portray>=1.3.1"],
        "all": ["cleo>=0.7.6", "python-dotenv>=0.10.3", "portray>=1.3.1"],
    },
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
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Java Libraries",
    ],
)
