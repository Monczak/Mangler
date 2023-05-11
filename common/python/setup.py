from setuptools import setup, find_packages

setup(
    name="mangler-common",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "marshmallow>=3.19.0"
    ]
)