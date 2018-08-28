import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brycetools",
    version="0.0.3",
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
    install_requires= ["pandas==0.23.4",
                       "rawpy==0.11.0",
                       "Keras==2.1.6",
                       "xmltodict==0.11.0",
                       "tqdm==4.24.0",
                       "scipy==1.1.0",
                       "setuptools==39.1.0",
                       "numpy==1.15.0",
                       "imageio==2.3.0",
                       ]
)