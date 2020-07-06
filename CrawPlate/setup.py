import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "crawlplates",
    version = "0.0.1",
    author = "Stephen Zhang",
    author_email = "stephenzhangbupt@me.com",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
)