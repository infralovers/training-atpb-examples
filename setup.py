import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name="python-blog",
    version = "0.1",
    packages=find_packages(),
    description="Read the latest Real Python tutorials",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Real Python",
    author_email="office@realpython.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=['Flask'],
    include_package_data=True,
    zip_safe=False
)
