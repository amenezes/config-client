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
    license='Apache-2.0',
    url="https://github.com/amenezes/config-client",
    packages=setuptools.find_packages(),
    python_requires='>=3.6.0',
    project_urls=OrderedDict((
        ('Documentation', 'https://github.com/amenezes/config-client'),
        ('Code', 'https://github.com/amenezes/config-client'),
        ('Issue tracker', 'https://github.com/amenezes/config-client/issues')
    )),
    install_requires=[
        'attrs>=19.1.0',
        'glom>=19.2.0',
        'requests>=2.22.0'
    ],
    extras_require={
        "cli": [
            'cleo>=0.7.6',
            'PyYAML>=5.3'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: AsyncIO",
        "Framework :: Flask",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Java Libraries",
    ],
)
