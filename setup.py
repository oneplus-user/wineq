from setuptools import setup, find_packages
# find_packages() automatically finds __init__.py file in my project directory 
# and help to create package
# we have __init__.py file in only 2 folder: src and tests

# setup() is used to provide the package metadata:
# package_name, version, description, license of my package
setup(
    name="wine_src",
    version="0.0.1",
    description="its a wine quality package", 
    author="oneplus-user", 
    packages=find_packages(),
    license="MIT"
)
