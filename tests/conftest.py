r""" tests.conftest module """


# importing standard modules ==================================================
import sys
from os.path import dirname, join
# adding the 'src' directory to path - HACK
sys.path.append(
    join(dirname(dirname(__file__)), "src")
)
