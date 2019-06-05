import setuptools

from collections import OrderedDict


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="config-client",
    version="0.2.0",
    author="alexandre menezes",
    author_email="alexandre.fmenezes@gmail.com",
    description="config service client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amenezes/config-client",
    packages=setuptools.find_packages(),
    project_urls=OrderedDict((
        ('Documentation', 'https://github.com/amenezes/config-client'),
        ('Code', 'https://github.com/amenezes/config-client'),
        ('Issue tracker', 'https://github.com/amenezes/config-client/issues')
    )),
    install_requires=[
        'requests>=2.22.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: AsyncIO",
        "Framework :: Flask",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
