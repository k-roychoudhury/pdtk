r""" tests.conftest module """


# importing standard modules ==================================================
from os.path import dirname, join
import sys

# adding the 'src' directory to path - HACK
sys.path.append(
    join(dirname(dirname(__file__)), "src")
)
