import io
import os
import sys
from shutil import rmtree

from setuptools import setup, Command

# Package meta-data.
NAME = "timesoft"
DESCRIPTION = "Python 3.9+ TimeSoft"
URL = "https://github.com/yurii-bel/project_2021"
EMAIL = "info@timesoft.pp.ua"
AUTHOR = "Symonovsky I.V., Beliavtsev Y.V., Vergun D.O., Kolesnykov Y.D., Lastivka T.T., Tyron V.V., Pechkur O.A."
REQUIRES_PYTHON = ">=3.9.0"
VERSION = "2021.05.28"
REQUIRED = ["psycopg2>=2.8.6", "PyQt5>=5.15.4",
            "pyqtgraph>=1.1.0", "pandas>=1.2.4"]


here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel distribution…")
        os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        print("Uploaded ...")
        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    packages=["timesoft"],
    install_requires=REQUIRED,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email=EMAIL,
    package_dir={"timesoft": "timesoft"},
    include_package_data=True,
    py_modules=["timesoft"],
    url=URL,
    license="Public License",
    keywords="""
				python3
				timesoft
               """,
    python_requires=REQUIRES_PYTHON,
    zip_safe=False,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 5 - Production/Stable",
        "Framework :: PyQt5",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    # Build and upload package: `python3 setup.py upload`
    cmdclass={"upload": UploadCommand},
)
print("Success install ...")
