"""Setup script for predicate_bst package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="predicate_bst",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    description="Convert logical statements to Boolean syntax trees",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Evan Ochsner",
    author_email="evan.ochsner@gmail.com",
    url="https://github.com/EvanOchsner/predicate-bst",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "polars>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
)