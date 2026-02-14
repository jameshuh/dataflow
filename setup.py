from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dataflow-converter",
    version="0.1.0",
    author="James Hu",
    author_email="3305363@qq.com",
    description="A powerful data format conversion tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jameshuh/dataflow",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
        "PyYAML>=5.4.0",
        "click>=8.0.0",
        "lxml>=4.6.0",
    ],
    entry_points={
        "console_scripts": [
            "dataflow=dataflow.cli:main",
        ],
    },
)
