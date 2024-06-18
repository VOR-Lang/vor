import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="vorlang",
    version="0.0.2-alpha",
    author="Vorlang",
    author_email="me@zanderlewis.dev",
    description="The VOR Programming Language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    repository="https://github.com/VOR-Lang/vor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["vor=vorlang.main:main"]},
    python_requires=">=3.6",
)
