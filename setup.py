from setuptools import setup

__author__ = 'TRAN QUANG HUY'
__copyright__ = 'Copyright (C) 2019, Intek Institute'
__email__ = 'huy.tran@f4.intek.edu.vn'
__license__ = 'MIT'
__maintainer__ = 'TRAN QUANG HUY'
__version__ = '1.0.6'
__name__ = "spritessheettquang97"


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author=__author__,
    author_email=__email__,
    name= __name__,
    copyright = __copyright__,
    license = __license__,
    maintainer = __maintainer__,
    version = __version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["spritessheettquang97"],
    include_package_data=True,
    install_requires=[
        "numpy==1.18.1",
        "Pillow==8.1.1 ",
    ]
)