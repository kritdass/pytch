from setuptools import setup

setup(
    name="pytch",
    version="0.1.0",
    author="Krit Dass",
    author_email="dasskrit@gmail.com",
    url="https://github.com/kritdass/pytch",
    description="A lightweight and elegant fetch written in Python with 0 dependencies.",
    packages=["pytch"],
    entry_points={"console_scripts": ["pytch = pytch.pytch:main"]},
)
