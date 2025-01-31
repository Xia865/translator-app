from setuptools import setup, find_packages

setup(
    name="translator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "googletrans==3.1.0a0",
    ],
    scripts=['bin/translator'],
)