import os

from setuptools import setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), "r") as f:
    long_description = f.read()


setup(
    name="magic_logger",
    py_modules=["magic_logger"],
    version="1.0.0",
    license="MIT",
    description="Helps you use logging correctly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Radu Ghitescu",
    author_email="radu.ghitescu@gmail.com",
    url="https://github.com/RaduG/magic_logger",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    zip_safe=False,
)