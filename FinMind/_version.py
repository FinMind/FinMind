from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__.replace("._version", ""))
except PackageNotFoundError:
    __version__ = "0.0.0.nof"
