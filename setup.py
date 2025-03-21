"""Setup script for predicate_to_bst package."""

from setuptools import setup, find_packages

setup(
    name="predicate_to_bst",
    version="0.1.0",
    packages=find_packages(),
    description="Convert logical statements to Boolean syntax trees",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/predicate_to_bst",
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
    install_requires=[],
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
