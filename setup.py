from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

VERSION = '0.0.1'
DESCRIPTION = 'A command line tool to manipulate JSON files.'

setup(
    name="jsonwiz",
    version=VERSION,
    author="Karishma Shukla",
    author_email="karishmashuklaa@gmail.com",
    url="https://github.com/karishmashuklaa/jsonwiz",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description= readme(),
    packages=find_packages(),
    keywords=[
        "json",
        "cli",
        "command line",
        "command line interface",
        "json files",
        "json manipulation",
        "jsoncli",
        "jsoncli tool",
        "jsoncli command line tool",
        "jsoncli command line interface",
        "jsonwiz",
        "jsonwiz tool",
        "jsoncli command line",
    ],
    entry_points={
        'console_scripts': [
            'jsonwiz = jsonwiz.__init__:main'
        ]
    },
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)