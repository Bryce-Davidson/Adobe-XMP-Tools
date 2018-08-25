import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brycetools",
    version="0.0.2",
    author="Bryce Davidson",
    author_email="bryce_davidson@icloud.com",
    description="bryce tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BryceDavidson/brycetools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)