import shutil
import os

from dropbox import get_dropbox_path_business
from output import log


def _publish_to_dropbox(source_file: str, destination_file: str, replace: bool = True):
    """
    Copies `source_file` to `destination_file` (which is relative to the Dropbox business folder).

    Parameters
    ----------
    source_file : str
        Path to the source file.
    destination_file : str
        Path to the destination, relative to the dropbox folder location.
    replace: bool = True
        True to copy the file even if it exists in the destination.
    """
    dropbox = get_dropbox_path_business()
    pub_path = os.path.abspath(f'{dropbox}/{destination_file}')
    if os.path.exists(pub_path) and not replace:
        return
    source_file = os.path.abspath(source_file)
    shutil.copyfile(source_file, pub_path)
    log(f'Published "{source_file}"\n'
        f'       to "{pub_path}".')


def _publish_local(source_file: str, destination_file: str, replace: bool = True):
    """
    Copies `source_file` to `destination_file`.

    Parameters
    ----------
    source_file : str
        Path to the source file.
    destination_file : str
        Path to the destination.
    replace: bool = True
        True to copy the file even if it exists in the destination.
    """
    source_file = os.path.abspath(source_file)
    destination_file = os.path.abspath(destination_file)
    if os.path.exists(destination_file) and not replace:
        return
    shutil.copyfile(source_file, destination_file)
    log(f'Published "{source_file}"\n'
        f'       to "{destination_file}".')


def publish(source_file: str, destination: str, replace: bool = True):
    """
    Publish `source_file` to `destination`. Supports multiple endpoints:

    Endpoints
    ---------
    If `destination` starts with "dropbox::", the file is copied to a location in your
    Dropbox business folder.

    Any other `destination` is assumed to be a local path.

    Parameters
    ----------
    source_file : str
        Path to the source file.
    destination : str
        Path to the destination end point.
    replace: bool = True
        True to publish the file even if it exists in the destination.
    """

    if destination.startswith("dropbox::"):
        _publish_to_dropbox(source_file, destination.replace('dropbox::', '/'), replace)
    else:
        _publish_local(source_file, destination, replace)
