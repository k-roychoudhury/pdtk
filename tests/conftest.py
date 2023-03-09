r""" tests.conftest module """

from os.path import dirname, join
import sys

# adding the 'src' directory to path
sys.path.append(
    join(dirname(dirname(__file__)), "src")
)

