VERSION: str

try:
    from foodprep.__version__ import __version__ as VERSION  # type: ignore
except ModuleNotFoundError:
    from setuptools_scm import get_version  # type: ignore

    VERSION = get_version(root="..", relative_to=__file__, local_scheme="dirty-tag")
