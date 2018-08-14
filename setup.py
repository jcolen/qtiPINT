import os
import sys

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup
    setup


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


setup(
    name="qtiPINT",
    version='2015.11',
    author="Jonathan Colen",
    author_email="jcolen19@gmail.com",
    packages=["qtipint"],
    url="http://github.com/jcolen/qtiPINT/",
    license="GPLv3",
    description="Qt Interface for PINT Pulsar timing",
    long_description=open("README.md").read() + "\n\n"
                    + "Changelog\n"
                    + "---------\n\n"
                    + open("HISTORY.md").read(),
    package_data={"": ["LICENSE", "AUTHORS.md"]},
    include_package_data=True,
    install_requires=["numpy", "scipy", "h5py"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
