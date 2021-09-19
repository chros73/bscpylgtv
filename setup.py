from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="aiopylgtv",
    packages=["aiopylgtv"],
    install_requires=["websockets>=8.1", "numpy>=1.17.0", "sqlitedict"],
    python_requires=">=3.7",
    zip_safe=True,
    version="0.4.1",
    description="Library to control webOS based LG TV devices.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Josh Bendavid",
    author_email="joshbendavid@gmail.com",
    url="https://github.com/bendavid/aiopylgtv",
    keywords=["webos", "tv"],
    classifiers=[],
    entry_points={
        "console_scripts": ["aiopylgtvcommand=aiopylgtv.utils:aiopylgtvcommand"]
    },
)
