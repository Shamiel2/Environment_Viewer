import setuptools

setuptools.setup(
    name="environment_viewer",
    version="0.1.0",
    description="A Tool were you can View, Create and Modify your Environment Variables with a given DCC."
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    url='https://github.com/Shamiel2/Environment_Viewer.git',
)