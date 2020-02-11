import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryptonote-address-validator",
    version="1.0.0",
    author="Mosu Forge",
    author_email="mosu.forge@protonmail.com",
    description="Validate cryptonote addresses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ragerxlol/cryptonote-address-validator-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
