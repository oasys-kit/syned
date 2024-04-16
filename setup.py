#! /usr/bin/env python3

import os

try:
    from setuptools import find_packages, setup
except AttributeError:
    from setuptools import find_packages, setup

NAME = 'syned'

VERSION = '1.0.40'
ISRELEASED = True

DESCRIPTION = 'SYNED (SYNchrotron Elements Dictionary) kernel library'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.rst')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Manuel Sanchez del Rio, Luca Rebuffi'
AUTHOR_EMAIL = 'srio@esrf.eu'
URL = 'https://github.com/oasys-kit/syned'
DOWNLOAD_URL = 'https://github.com/oasys-kit/syned'
MAINTAINER = 'L Rebuffi and M Sanchez del Rio'
MAINTAINER_EMAIL = 'srio@esrf.eu'
LICENSE = 'GPLv3'

KEYWORDS = (
    'dictionary',
    'glossary',
    'synchrotron'
    'simulation',
)

CLASSIFIERS = (
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: '
    'GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
)

INSTALL_REQUIRES = (
    'setuptools',
    'numpy',
    'scipy',
)

SETUP_REQUIRES = (
    'setuptools',
)

PACKAGES = [
    "syned",
    "syned.beamline",
    "syned.beamline.optical_elements",
    "syned.beamline.optical_elements.absorbers",
    "syned.beamline.optical_elements.crystals",
    "syned.beamline.optical_elements.gratings",
    "syned.beamline.optical_elements.ideal_elements",
    "syned.beamline.optical_elements.mirrors",
    "syned.beamline.optical_elements.refractors",
    "syned.beamline.optical_elements.ideal_elements",
    "syned.beamline.optical_elements.ideal_elements",
    "syned.storage_ring",
    "syned.storage_ring.magnetic_structures",
    "syned.util",
    "syned.widget",
]

PACKAGE_DATA = {
}


def setup_package():
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        url=URL,
        download_url=DOWNLOAD_URL,
        license=LICENSE,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        # extra setuptools args
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        setup_requires=SETUP_REQUIRES,
    )

if __name__ == '__main__':
    setup_package()
