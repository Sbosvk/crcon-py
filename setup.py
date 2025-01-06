from setuptools import setup, find_packages

setup(
    name="crcon-py",
    version="1.0.0",
    description="Python wrapper for the CRCON API ^11",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Oliver Krilov",
    author_email="sbosvk@gmail.com",
    url="https://github.com/Sbosvk/crcon-py",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
