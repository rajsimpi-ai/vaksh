from setuptools import setup, find_packages

setup(
    name="vaksh",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # add deps here later (openai, groq, etc.)
    ],
    entry_points={
        "console_scripts": [
            "vak=vaksh.main:main",  # this exposes the "vak" command
        ],
    },
    author="Your Name",
    description="VakSh: Speech to Shell, Words to Power",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rajsimpi-ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)