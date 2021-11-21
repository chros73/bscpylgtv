from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="bscpylgtv",
    packages=["bscpylgtv"],
    install_requires=["websockets>=8.1", "sqlitedict"],
    python_requires=">=3.7",
    zip_safe=True,
    version="0.1.1",
    description="Library to control webOS based LG TV devices.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="chros",
    author_email="chros73@gmail.com",
    url="https://github.com/chros73/bscpylgtv",
    keywords=["webos", "tv"],
    classifiers=[],
    entry_points={
        "console_scripts": ["bscpylgtvcommand=bscpylgtv.utils:bscpylgtvcommand"]
    },
)
